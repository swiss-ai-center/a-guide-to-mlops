"""Split the generated planet dataset into per-class data and an optional obfuscated inference set.

The script takes the output of ``generate_planet_dataset_simply.py`` (``dataset/``)
and creates:

* ``data/<class>/`` — a balanced set of sampled images for each configured
  class.
* ``extra-data/extra/`` — all remaining images (unused images from the selected
  classes plus all images from the withheld classes). Pass ``--encode`` to
  obfuscate filenames with a reversible, reversed base64 encoding so the
  filename no longer reveals the class and adjacent files in the directory
  listing come from random categories.

The encoding is reversible from the filename alone; no separate mapping file is
required. Use ``--decode`` to restore the original names.

Usage:
    python split_dataset.py \
        --input dataset \
        --output-data data \
        --output-extra extra-data/extra \
        --train-classes Mercury Venus Earth Mars Jupiter Saturn Uranus Neptune Moon Pluto \
        --images-per-class 80 \
        --seed 42 \
        --encode

Decode obfuscated inference names back to their originals:
    python split_dataset.py --decode --decode-dir extra-data/extra
"""

from __future__ import annotations

import argparse
import base64
import random
import shutil
import sys
from pathlib import Path


# ---------------------------------------------------------------------------
# Filename encoding helpers
#
# Based on encode_decode.py from the a-guide-to-mlops repository:
# https://raw.githubusercontent.com/swiss-ai-center/a-guide-to-mlops/
#     refs/heads/extra-data/encode_decode.py
# ---------------------------------------------------------------------------


def encode_filename(stem: str) -> str:
    """Encode a filename stem with reversed, URL-safe base64 without padding.

    The base64 string is reversed so the high-entropy end (the image index)
    becomes the filename prefix. This scatters images from the same class
    across a sorted directory listing.
    """
    encoded = base64.urlsafe_b64encode(stem.encode()).decode().rstrip("=")
    return encoded[::-1]


def decode_filename(encoded_stem: str) -> str:
    """Decode a filename stem produced by ``encode_filename``.

    Reverse the encoded stem back to its original base64 form, restore
    padding, and base64-decode it.
    """
    reversed_stem = encoded_stem[::-1]
    padding_needed = 4 - (len(reversed_stem) % 4)
    padded = reversed_stem + ("=" * padding_needed)
    return base64.urlsafe_b64decode(padded.encode()).decode()


# ---------------------------------------------------------------------------
# Core splitting logic
# ---------------------------------------------------------------------------


def split_dataset(
    input_dir: Path,
    output_data_dir: Path,
    output_extra_dir: Path,
    train_classes: list[str],
    images_per_class: int,
    seed: int,
    move_extra: bool = False,
    overwrite: bool = False,
    encode_extra: bool = False,
) -> None:
    """Split a raw planet dataset into per-class data and optional obfuscated inference set."""
    rng = random.Random(seed)

    if not input_dir.is_dir():
        raise FileNotFoundError(f"Input directory does not exist: {input_dir}")

    missing = [c for c in train_classes if not (input_dir / c).is_dir()]
    if missing:
        raise FileNotFoundError(
            f"Missing class directories in {input_dir}: {', '.join(missing)}"
        )

    # Discover all classes present in the raw dataset.
    all_classes = sorted(
        p.name for p in input_dir.iterdir() if p.is_dir() and not p.name.startswith(".")
    )
    drift_classes = sorted(set(all_classes) - set(train_classes))
    if not drift_classes:
        print("Warning: no drift classes found; all classes are in --train-classes.")

    if output_extra_dir.exists() and any(output_extra_dir.iterdir()):
        if not overwrite:
            raise FileExistsError(
                f"{output_extra_dir} already exists and is not empty. "
                "Pass --overwrite to replace its contents."
            )
        for item in output_extra_dir.iterdir():
            if item.is_dir():
                shutil.rmtree(item)
            else:
                item.unlink()

    output_extra_dir.mkdir(parents=True, exist_ok=True)

    all_extra_images: list[Path] = []
    selected_by_class: dict[str, list[Path]] = {}

    # ------------------------------------------------------------------
    # Copy sampled images for each selected class into the output class dir.
    # If the output dir is the same as the input dir, this reorganises the
    # raw data in place by removing the unselected images.
    # ------------------------------------------------------------------
    for class_name in train_classes:
        class_dir = input_dir / class_name
        images = sorted(class_dir.glob("*.jpg"))
        if not images:
            raise FileNotFoundError(f"No images found in {class_dir}")
        if len(images) < images_per_class:
            raise ValueError(
                f"Class {class_name} has only {len(images)} images, "
                f"but --images-per-class is {images_per_class}."
            )

        selected = rng.sample(images, images_per_class)
        extra_images = [img for img in images if img not in set(selected)]

        selected_by_class[class_name] = selected
        all_extra_images.extend(extra_images)

        print(f"{class_name}: {len(selected)} data, {len(extra_images)} extra")

    # ------------------------------------------------------------------
    # All images from the withheld/drift classes go to extra-data.
    # ------------------------------------------------------------------
    for class_name in drift_classes:
        class_dir = input_dir / class_name
        images = sorted(class_dir.glob("*.jpg"))
        all_extra_images.extend(images)
        print(f"{class_name}: {len(images)} extra (drift class)")

    # ------------------------------------------------------------------
    # Copy/move all inference images to extra-data first, before altering the
    # output class directories. This ensures in-place reorganisation does not
    # delete extras before they have been copied.
    # ------------------------------------------------------------------
    rng.shuffle(all_extra_images)
    _move_or_copy_extra(all_extra_images, output_extra_dir, move_extra, encode_extra)

    # ------------------------------------------------------------------
    # Populate the output class directories with the selected samples.
    # ------------------------------------------------------------------
    for class_name, selected in selected_by_class.items():
        class_output_dir = output_data_dir / class_name
        class_output_dir.mkdir(parents=True, exist_ok=True)

        in_place = class_output_dir.resolve() == (input_dir / class_name).resolve()
        selected_set = set(selected)

        for existing in class_output_dir.glob("*.jpg"):
            if existing not in selected_set:
                existing.unlink()

        if not in_place:
            for img in selected:
                shutil.copy2(img, class_output_dir / img.name)

    # When reorganising in place, remove drift class directories so the output
    # data directory contains only the selected classes.
    if output_data_dir.resolve() == input_dir.resolve():
        for class_name in drift_classes:
            drift_dir = output_data_dir / class_name
            if drift_dir.exists():
                shutil.rmtree(drift_dir)

    total_data = sum(
        len(list((output_data_dir / c).glob("*.jpg"))) for c in train_classes
    )
    total_extra = len(all_extra_images)

    print("\nDataset split complete:")
    print(f"  Data:       {total_data} images in {output_data_dir}")
    print(f"  Inference:  {total_extra} images in {output_extra_dir}")


def _move_or_copy_extra(
    images: list[Path],
    output_extra_dir: Path,
    move: bool,
    encode: bool,
) -> None:
    """Copy or move inference images to extra-data, optionally encoding their names."""
    used_names: set[str] = set()

    for img in images:
        if encode:
            new_stem = encode_filename(img.stem)
        else:
            new_stem = img.stem
        new_name = f"{new_stem}{img.suffix}"

        # Guard against filename collisions (relevant both with and without encoding).
        if new_name in used_names:
            raise ValueError(
                f"Filename collision for {img.name}. "
                "The input contains duplicate stems."
            )
        used_names.add(new_name)

        dst = output_extra_dir / new_name
        if move:
            shutil.move(img, dst)
        else:
            shutil.copy2(img, dst)


def decode_directory(directory: Path) -> None:
    """Decode all reversed-base64 filenames in a directory back to their originals.

    Files are renamed in place; no subfolders are created and no train/val
    split is performed.
    """
    if not directory.is_dir():
        raise FileNotFoundError(f"Directory does not exist: {directory}")

    decoded = 0
    skipped = 0
    for file in sorted(directory.iterdir()):
        if not file.is_file():
            continue

        try:
            original_stem = decode_filename(file.stem)
        except Exception as e:
            print(f"Skipping {file.name}: could not decode ({e})")
            skipped += 1
            continue

        new_name = f"{original_stem}{file.suffix}"
        new_path = file.with_name(new_name)
        if new_path.exists():
            print(f"Skipping {file.name}: target {new_name} already exists.")
            skipped += 1
            continue

        file.rename(new_path)
        decoded += 1

    print(f"Decoded {decoded} filenames in {directory} ({skipped} skipped).")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Split a generated planet dataset into per-class data and an "
                    "optional obfuscated inference set, or decode obfuscated "
                    "inference filenames back to their originals."
    )
    parser.add_argument(
        "--input",
        type=Path,
        default=Path("dataset"),
        help="Directory containing the full generated dataset (default: dataset).",
    )
    parser.add_argument(
        "--output-data",
        type=Path,
        default=Path("data"),
        help="Root directory for the per-class data folders (default: data).",
    )
    parser.add_argument(
        "--output-extra",
        type=Path,
        default=Path("extra-data/extra"),
        help="Directory for the obfuscated inference set (default: extra-data/extra).",
    )
    parser.add_argument(
        "--train-classes",
        nargs="+",
        default=[
            "Mercury", "Venus", "Earth", "Mars", "Jupiter",
            "Saturn", "Uranus", "Neptune", "Moon", "Pluto",
        ],
        help="Classes placed in the output data directory (default: 8 planets + Moon + Pluto).",
    )
    parser.add_argument(
        "--images-per-class",
        type=int,
        default=80,
        help="Number of images to sample per class (default: 80).",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Random seed for reproducible sampling and splitting (default: 42).",
    )
    parser.add_argument(
        "--move",
        action="store_true",
        help="Move inference images to extra-data instead of copying them.",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite existing output directories if they are not empty.",
    )
    parser.add_argument(
        "--encode",
        action="store_true",
        help="Encode inference filenames in extra-data with reversed base64.",
    )
    parser.add_argument(
        "--decode",
        action="store_true",
        help="Decode obfuscated filenames back to their original names.",
    )
    parser.add_argument(
        "--decode-dir",
        type=Path,
        default=None,
        help="Directory to decode (default: the value of --output-extra).",
    )
    args = parser.parse_args()

    if args.decode:
        decode_dir = args.decode_dir or args.output_extra
        decode_directory(decode_dir)
        return

    split_dataset(
        input_dir=args.input,
        output_data_dir=args.output_data,
        output_extra_dir=args.output_extra,
        train_classes=args.train_classes,
        images_per_class=args.images_per_class,
        seed=args.seed,
        move_extra=args.move,
        overwrite=args.overwrite,
        encode_extra=args.encode,
    )


if __name__ == "__main__":
    main()
