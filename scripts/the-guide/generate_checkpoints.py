import os
import re
import shutil
import subprocess
import textwrap
from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import List, Union

import yaml

GENERAION_OUTPUT_FILENAME = "generation_output.md"


def esc(code: Union[str, int]) -> str:
    """Get escape code."""
    return f"\033[{code}m"


def write_output(output: str) -> None:
    """Write output to file."""
    with open(GENERAION_OUTPUT_FILENAME, "+a") as f:
        f.write(output + "\n")


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
        print(esc(94), f"Running command: {self.command}", esc(0), sep="")
        task = subprocess.Popen(self.command, shell=True, stdout=subprocess.PIPE)
        data = task.stdout.read().decode("utf-8")
        if data:
            print(esc(90), data, esc(0))
        if self.log_output:
            print(esc(94), f"  Log output: {self.log_output}", esc(0), sep="")
            write_output(f"> {self.command}\n")
            write_output(f"```\n{data}```\n")
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
        print(esc(94), f"Replacing file: {self.file_path}", esc(0), sep="")
        print(esc(94), f"  From md: {self.md_path}", esc(0), sep="")
        print(esc(94), f"  Occurance index: {self.occurance_index}", esc(0), sep="")

        regex = rf'```.* title="{re.escape(str(self.file_path))}".*\n([\s\S]*?)```$'
        content = self.abs_md_path.read_text()
        matches = re.findall(regex, content, re.MULTILINE)
        if not matches:
            raise ValueError(
                f"Could not find code block file in md: {str(self.file_path)}"
            )
        to_replace = textwrap.dedent(matches[self.occurance_index])

        if not self.file_path.exists():
            os.makedirs(self.file_path.parent, exist_ok=True)
        self.file_path.write_text(to_replace)


@dataclass
class Save:
    """A save is a collection of actions to run and a path to save the result."""

    tmp_path: Path
    save_path: Path
    save_git: bool
    actions: List[AbstractAction]

    def __post_init__(self) -> None:
        self.name = self.save_path.name
        self.tmp_path = self.tmp_path.resolve()
        self.save_path = self.save_path.resolve()

    def run_and_save(self) -> None:
        print(esc("92;1"), f"\nRunning save: {self.name}", esc(0), sep="")
        for action in self.actions:
            action.run()

        if self.save_git:
            # Copy all files, ignore by gitignore and unstaged files
            shutil.copytree(
                ".",
                self.save_path,
                ignore=self._get_ignored_as_git,
                dirs_exist_ok=True,
            )
        else:
            # Copy all files
            shutil.copytree(
                self.tmp_path,
                self.save_path,
                ignore=shutil.ignore_patterns(".git", GENERAION_OUTPUT_FILENAME),
                dirs_exist_ok=True,
            )

    def _get_ignored_as_git(self, path: str, filenames: List[str]) -> List[str]:
        """
        Get files and directories to ignore as gitignore and unstaged files.
        Simulates the state of a git repository.
        """

        to_exclude = set(
            [
                ".git",
                GENERAION_OUTPUT_FILENAME,
            ]
            + self._get_gitignored_patterns()
            + self._get_unstaged_patterns()
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

    base_tmp_path: Path
    saves: List[Save]

    def run(self) -> None:
        if self.base_tmp_path.exists():
            shutil.rmtree(self.base_tmp_path)

        self.base_tmp_path.mkdir(parents=True, exist_ok=True)
        os.chdir(self.base_tmp_path)

        write_output(f"# Generation Output\n")
        for save in self.saves:
            write_output(f"## {save.name}\n")
            save.run_and_save()


@dataclass
class SavesFactory:
    """A factory for creating saves."""

    base_tmp_path: Path
    base_save_path: Path

    def create(self, saves: dict) -> List[Save]:
        return [self._create_save(save_dir, save) for save_dir, save in saves.items()]

    def _create_save(self, save_dir: str, save: dict) -> Save:
        save_path = self.base_save_path / save_dir
        save_path.mkdir(parents=True, exist_ok=True)

        actions = []
        for action in save["actions"]:
            if "run" in action:
                actions.append(
                    CommandAction(
                        command=action["run"],
                        log_output=action.get("log", False),
                    )
                )
            elif "replace_from_md" in action:
                pass
                actions.append(
                    ReplaceFileFromMdAction(
                        file_path=Path(action["file"]),
                        md_path=save_path / action.get("md_path", "index.md"),
                        occurance_index=action["occurance_index"],
                    )
                )
            else:
                raise ValueError(f"Unknown action type in: {action.keys()}")

        return Save(self.base_tmp_path, save_path, save["save_git"], actions)


def main() -> None:
    """
    The main entry point for the guide generation script.

    It creates a new tmp directory, runs the actions and saves the result in the save directory.
    All actions are defined in the actions.yaml file and are run in the tmp working directory.

    The actions.yaml file is structured as follows:

    ```yaml
    base_tmp_path: The path to the tmp directory
    base_save_path: The path to the save directory

    saves:
        <save_dir>: # The directory to save the result in
            save_git: True # Whether to save the gitignored files
            actions:
                - run: <command> # Run a command
                    log: True # Whether to log the output
                - replace_from_md: # Replace a file with a code block from a markdown file
                    file: <file_path> # The path to the file to replace
                    md_path: <md_path> # The path to the markdown file
                    occurance_index: <occurance_index> # The index of the code block to use
    ```

    The output of the actions is saved in the GENERAION_OUTPUT_FILENAME file (see top of file).
    """
    actions = yaml.safe_load(Path("scripts/the-guide/actions.yaml").read_text())

    base_tmp_path = Path(actions["base_tmp_path"])
    base_save_path = Path(actions["base_save_path"])
    saves_factory = SavesFactory(base_tmp_path, base_save_path)

    saves = saves_factory.create(saves=actions["saves"])
    saves_manager = SavesManager(base_tmp_path=base_tmp_path, saves=saves)

    saves_manager.run()


if __name__ == "__main__":
    main()
