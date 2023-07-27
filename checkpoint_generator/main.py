import argparse
import os
import re
import shutil
import subprocess
import sys
import textwrap
from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Union

import yaml

GENERATED_OUTPUT_PATH = "../generated_output.md"


def esc(code: Union[str, int]) -> str:
    """Get escape code."""
    return f"\033[{code}m"


def write_output(output: str) -> None:
    """Write output to file."""
    with open(GENERATED_OUTPUT_PATH, "+a") as f:
        f.write(output + "\n")


def error(msg: str) -> None:
    """Print error and exit."""
    print("\n", esc(31), msg, esc(0), sep="", file=sys.stderr)
    exit(1)


@dataclass
class AbstractAction(ABC):
    def __post_init__(self) -> None:
        if self.__class__ == AbstractAction:
            raise TypeError("Cannot instantiate abstract class.")

    @abstractmethod
    def run(self) -> None:
        pass


@dataclass
class CommandAction(AbstractAction):
    """Run and logs a command."""

    command: str
    log_output: bool = False

    def run(self) -> None:
        print(esc(94), f"[RUN] {self.command}", esc(0), sep="")
        task = subprocess.Popen(
            self.command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        out, err = [c.decode("utf-8") for c in task.communicate()]
        if task.returncode != 0:
            error(f"Command failed: {self.command}\n{err}")
        if out:
            print(esc(90), out, esc(0), sep="")
        if self.log_output:
            write_output(f"> {self.command}\n")
            write_output(f"```\n{out}```\n")
            write_output(f"----\n")


@dataclass
class ReplaceFileFromMdAction(AbstractAction):
    """Replace a file with the content of a code block in a md file."""

    file_path: Path
    md_path: Path
    occurance_index: int

    def __post_init__(self) -> None:
        # We resolve only the md path, because the file path is relative to tmp
        # working directory (current working directory)
        self.abs_md_path = self.md_path.resolve()
        if not self.md_path.exists():
            raise ValueError(f"Md file does not exist: {self.md_path}")

    def run(self) -> None:
        print(
            esc(94),
            f"[REPLACE FROM MD] {self.file_path} <- {self.md_path}",
            esc(0),
            sep="",
        )

        regex = rf'```.* title="{re.escape(str(self.file_path))}".*\n([\s\S]*?)```$'
        content = self.abs_md_path.read_text()
        matches = re.findall(regex, content, re.MULTILINE)
        if not matches:
            raise ValueError(f"Could not find code block in md: {str(self.md_path)}")

        to_replace = textwrap.dedent(matches[self.occurance_index])

        if not self.file_path.exists():
            os.makedirs(self.file_path.parent, exist_ok=True)
        self.file_path.write_text(to_replace)


@dataclass
class Save:
    """A save is a collection of actions to run and a path to save the result."""

    abs_wd_tmp_path: Path
    abs_save_path: Path
    save_git: bool
    actions: List[AbstractAction]

    def __post_init__(self) -> None:
        self.name = self.abs_save_path.name

    def run(self) -> None:
        print(esc("92;1"), f"\nRunning action for save: {self.name}", esc(0), sep="")
        for action in self.actions:
            action.run()

    def save(self) -> None:
        self.abs_save_path.mkdir(parents=True, exist_ok=True)
        if self.save_git:
            # Copy all files, ignore by gitignore and unstaged files
            shutil.copytree(
                ".",
                self.abs_save_path,
                ignore=self._get_ignored_as_git,
                dirs_exist_ok=True,
            )
        else:
            # Copy all files
            shutil.copytree(
                self.abs_wd_tmp_path,
                self.abs_save_path,
                ignore=shutil.ignore_patterns(".git"),
                dirs_exist_ok=True,
            )

    def _get_ignored_as_git(self, path: str, filenames: List[str]) -> List[str]:
        """
        Get files and directories to ignore as gitignore and unstaged files.
        Simulates the state of a git repository.
        """

        to_exclude = set(
            [".git"] + self._get_gitignored_patterns() + self._get_unstaged_patterns()
        )
        ret = []
        for filename in filenames:
            if str(Path(path) / filename) in to_exclude:
                ret.append(filename)
        return ret

    def _get_gitignored_patterns(self) -> List[str]:
        """Get gitignored files and directories"""

        gitignored_files = subprocess.check_output(
            "git ls-files --others --ignored --exclude-standard --directory", shell=True
        )
        return [str(Path(p)) for p in gitignored_files.decode("utf-8").splitlines()]

    def _get_unstaged_patterns(self) -> List[str]:
        """Get unstaged/untracked files and directories"""

        unstaged_files = subprocess.check_output(
            "git ls-files --others --modified --exclude-standard --directory",
            shell=True,
        )
        return [str(Path(p)) for p in unstaged_files.decode("utf-8").splitlines()]


@dataclass
class SavesManager:
    """A manager for a collection of saves. Creates a temporary directory to run the saves in."""

    tmp_wd_path: Path
    saves: List[Save]
    clean_tmp: bool = False
    run_until: Optional[int] = None
    should_save: bool = True

    def run(self) -> None:
        cwd = Path.cwd()
        if self.tmp_wd_path.exists():
            shutil.rmtree(self.tmp_wd_path)

        self.tmp_wd_path.mkdir(parents=True, exist_ok=True)
        os.chdir(self.tmp_wd_path)

        if Path(GENERATED_OUTPUT_PATH).exists():
            os.remove(GENERATED_OUTPUT_PATH)

        write_output(f"# Generation Output\n")
        for i, save in enumerate(self.saves):
            if self.run_until is not None and i >= self.run_until:
                break
            write_output(f"## {save.name}\n")
            save.run()
            if self.should_save:
                save.save()

        os.chdir(cwd)
        if self.clean_tmp:
            shutil.rmtree(self.tmp_wd_path)


@dataclass
class SavesFactory:
    """A factory for creating saves."""

    tmp_wd_path: Path
    base_md_path: Path
    base_save_path: Path

    def create(self, saves: dict, variables: dict) -> List[Save]:
        return [
            self._create_save(md_path, save, variables)
            for md_path, save in saves.items()
        ]

    def _template_string(self, string: str, variables: dict) -> str:
        """Replace variables in a string under the format {{ variable }}"""
        for key, value in variables.items():
            string = string.replace("{{ " + key + " }}", str(value))
        return string

    def _create_save(self, md_path: str, save: dict, variables: dict) -> Save:
        """Create a Save instance from a dict"""
        md_full_path = self.base_md_path / md_path

        actions = []
        for action in save["actions"] or []:
            if "run" in action:
                actions.append(
                    CommandAction(
                        command=self._template_string(
                            string=action["run"], variables=variables
                        ),
                        log_output=action.get("log", False),
                    )
                )
            elif "replace_from_md" in action:
                actions.append(
                    ReplaceFileFromMdAction(
                        file_path=Path(action["file"]),
                        md_path=md_full_path,
                        occurance_index=action["occurance_index"],
                    )
                )
            else:
                raise ValueError(
                    f"Unknown action type in .yaml file: '{list(action.keys())[0]}'. "
                    "Available action types are 'run' and 'replace_from_md'."
                )

        return Save(
            abs_wd_tmp_path=self.tmp_wd_path.resolve(),
            abs_save_path=(self.base_save_path.resolve() / md_path).with_suffix(""),
            save_git=save["save_git"],
            actions=actions,
        )


def main() -> None:
    """
    The main entry point for the guide generation script.

    It creates a new tmp directory, runs the actions and saves the result in the save directory.
    All actions are defined in the actions.yaml file and are run in the tmp working directory.

    The actions.yaml file is structured as follows:

    ```yaml
    base_tmp_path: The path to the tmp directory
    base_md_path: The base path to the markdown files

    variables: # Variables to replace in the 'run' actions
        <variable_name>: <variable_value>

    saves:
        <md_file_path>: # The path to the markdown file
            save_git: True # Whether to save the gitignored files
            actions:
                - run: <command> # Run a command
                    log: True # Whether to log the output
                - replace_from_md: # Replace a file with a code block from a markdown file
                    file: <file_path> # The path to the file to replace
                    occurance_index: <occurance_index> # The index of the code block to use
    ```

    The output of the actions is saved in the GENERATED_OUTPUT_PATH file (see top of file)
    which is in the `base_tmp_path` directory.
    """
    actions = yaml.safe_load(Path("checkpoint_generator/actions.yaml").read_text())

    base_tmp_path = Path(actions["base_tmp_path"])
    base_md_path = Path(actions["base_md_path"])
    tmp_wd_path = base_tmp_path / "working-directory"

    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "-c",
        "--clean",
        help="Delete the tmp working directory after running the actions.",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "-u",
        "--until",
        help="Run the actions until the given save index. If not given, run all actions.",
        type=int,
        default=None,
    )
    parser.add_argument(
        "--no-save",
        help="Do not save the result of the actions.",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "--save-path",
        help="The path to the save directory.",
        type=str,
        default=base_tmp_path / "saves",
    )
    args = parser.parse_args()

    saves_factory = SavesFactory(
        tmp_wd_path=tmp_wd_path,
        base_md_path=base_md_path,
        base_save_path=Path(args.save_path),
    )

    saves = saves_factory.create(
        saves=actions["saves"], variables=actions.get("variables", {})
    )
    saves_manager = SavesManager(
        tmp_wd_path=tmp_wd_path,
        saves=saves,
        clean_tmp=args.clean,
        run_until=args.until,
        should_save=not args.no_save,
    )

    saves_manager.run()


if __name__ == "__main__":
    main()