# Generate Checkpoints

## Description

This script generates the checkpoints for the guide.

## Pre-requisites

If the `GOOGLE_APPLICATION_CREDENTIALS` environment variable is not set, you need to set it to the path of the service account key file.

```bash
export GOOGLE_APPLICATION_CREDENTIALS=<path_to_service_account_key_file>
```

## Usage

To run the script, you need to be in the root directory of the repository.



```bash
python3 scripts/the-guide/generate_checkpoints.py
```

You can see a list of all the available options by running:

```bash
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




    