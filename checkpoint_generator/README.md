# Generate Checkpoints

## Description

This script generates the checkpoints for the guide.

## Pre-requisites

If the `GOOGLE_APPLICATION_CREDENTIALS` environment variable is not set, you
need to set it to the path of the service account key file.

```bash
export GOOGLE_APPLICATION_CREDENTIALS=<path_to_service_account_key_file>
```

## Usage

To run the script, you need to be in the root directory of the repository.

```bash
python3 checkpoint_generator/main.py
```

You can see a list of all the available options by running:

```bash
python3 checkpoint_generator/main.py --help
```

```
usage: main.py [-h] [-c] [-u UNTIL] [--no-save] [--save-path SAVE_PATH]

options:
  -h, --help            show this help message and exit
  -c, --clean           Delete the tmp working directory after running the actions. (default: False)
  -u UNTIL, --until UNTIL
                        Run the actions until the given save index. If not given, run all actions. (default: None)
  --no-save             Do not save the result of the actions. (default: False)
  --save-path SAVE_PATH
                        The path to the save directory. (default: tmp/saves)
```

## Configuration

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

The output of the actions is saved in the GENERATED_OUTPUT_PATH file (see
`main.py`) which is in the `base_tmp_path` directory.
