"""
This script encodes the filename of all files in a directory to base64
without padding.
It is use to make the name of extra data seem "random".

Usage:
    python encode_decode.py encode
    python encode_decode.py decode
"""

import base64
import sys
from pathlib import Path


def encode_filename_to_base64(directory: str):
    path = Path(directory)
    if not path.is_dir():
        print(f"{directory} is not a valid directory.")
        return

    for file in path.iterdir():
        if file.is_file():
            filename_without_extension = file.stem
            encoded_filename = (
                base64.urlsafe_b64encode(filename_without_extension.encode())
                .decode()
                .rstrip("=")
            )
            new_filename = f"{encoded_filename}{file.suffix}"
            file.rename(path / new_filename)


def decode_filename_from_base64(directory: str):
    path = Path(directory)
    if not path.is_dir():
        print(f"{directory} is not a valid directory.")
        return

    for file in path.iterdir():
        if file.is_file():
            filename_without_extension = file.stem
            padding_needed = 4 - (len(filename_without_extension) % 4)
            filename_with_padding = filename_without_extension + ("=" * padding_needed)
            decoded_filename = base64.urlsafe_b64decode(
                filename_with_padding.encode()
            ).decode()
            new_filename = f"{decoded_filename}{file.suffix}"
            file.rename(path / new_filename)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Invalid number of arguments.")
        sys.exit(1)
    if sys.argv[1] == "encode":
        encode_filename_to_base64("extra_data")
    elif sys.argv[1] == "decode":
        decode_filename_from_base64("extra_data")
