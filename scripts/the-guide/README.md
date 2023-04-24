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

    The output of the actions is saved in the GENERATED_OUTPUT_PATH file (see top of file).


# Generate Checkpoints

## Description

This script generates the checkpoints for the guide.

## Usage

To run the script, you need to be in the root directory of the repository.

```
python3 scripts/the-guide/generate_checkpoints.py
```

You can see a list of all the available options by running:

```
python3 scripts/the-guide/generate_checkpoints.py --help
```

## Configuration

The actions.yaml file is structured as follows:

```yaml
base_tmp_path: <the path to the tmp directory>
base_save_path: <the path to the save directory>

saves:
  <save_dir>: # The directory to save the result in
    save_git: True # Whether to save the gitignored files
    actions:
      - run: <command> # Run a command
        log: true # Whether to log the output to GENERATED_OUTPUT_PATH
      - replace_from_md: # Replace a file with a code block from a markdown file
        file: <file_path> # The path to the file to replace
        md_path: <md_path> # The path to the markdown file
        occurance_index: <occurance_index> # The index of the code block to use
```

The output of the actions is saved in the GENERATED_OUTPUT_PATH file (see `generate_checkpoints.py`) which is at the parent directory of the tmp working directory.




    