# Dataset

This branch is only intended to keep the Python script that generates a synthetic image dataset of planets, dwarf planets, and moons using the **[SIMply](https://github.com/gbrydon/SIMply)** ray-tracing library.

The generator renders textured spheres (and Saturn's rings) from randomized camera angles and saves the images as `128 × 128` RGB JPEGs on a black background. Each planet is centered and consistently framed, viewed from a camera latitude between `-45°` and `+45°` of the equator with a small extra perspective offset. To reduce aliased outlines, it renders each image at `512 × 512` (4× the output size) and then downsamples to `128 × 128` with the Lanczos filter.

## What is generated

Each class gets a dedicated folder with `n` images named `<ClassName>_<N>.jpg`, where `n` is set by `--per-class`.

Example folder layout after generation:

```
dataset/
├── Mercury/
│   ├── Mercury_0.jpg
│   ├── Mercury_1.jpg
│   └── ...
├── Venus/
├── Earth/
└── ...
```

## Prerequisites

### 1. Clone the SIMply library

SIMply is **not** available on PyPI. Clone it into the project root so the generator can import it from the local `simply/` directory:

```bash
cd /path/to/a-guide-to-mlops
git clone https://github.com/gbrydon/SIMply.git simply
```

After cloning you should have:

```
a-guide-to-mlops/
├── simply/              # SIMply source code
├── generate_planet_dataset_simply.py
├── textures/            # texture maps
└── ...
```

### 2. Create a virtual environment

```bash
uv venv --python 3.11
```

### 3. Install Python packages

The generator assumes the required packages are already installed in the active environment. You can install them with:

```bash
source .venv/bin/activate
uv pip install numpy pillow opencv-python scipy astropy open3d pandas matplotlib
```

SIMply itself is imported directly from the cloned `simply/` directory, so no additional `pip install simply` is required.

### 4. Prepare texture maps

Place all texture files in a directory named `textures/` at the project root. The generator loads them relative to `textures/`.

Required texture files include:

```
textures/
├── 2k_mercury.jpg
├── 2k_venus_atmosphere.jpg
├── 2k_earth_daymap.jpg
├── 2k_earth_clouds.jpg
├── 2k_moon.jpg
├── 2k_mars.jpg
├── 2k_ceres_fictional.jpg
├── 2k_jupiter.jpg
├── 2k_saturn.jpg
├── 2k_saturn_ring_alpha.png
├── 2k_uranus.jpg
├── 2k_neptune.jpg
├── 2k_pluto.jpg
├── 2k_eris_fictional.jpg
├── 2k_haumea_fictional.jpg
├── 2k_makemake_fictional.jpg
```

## Running the generator

From the project root:

```bash
python generate_planet_dataset_simply.py \
    --output dataset \
    --per-class 250
```

### Anti-aliasing options

By default the generator renders at `512 × 512` (4× the output size) and downsamples to `128 × 128` using the Lanczos filter. You can tune this trade-off:

```bash
# Faster, slightly softer edges (render at 256 × 256)
python generate_planet_dataset_simply.py \
    --output dataset \
    --per-class 250 \
    --render-scale 2

# Use a softer, cheaper downsampling filter
python generate_planet_dataset_simply.py \
    --output dataset \
    --per-class 250 \
    --downsample-filter bilinear

# Disable anti-aliasing entirely (render directly at 128 × 128)
python generate_planet_dataset_simply.py \
    --output dataset \
    --per-class 250 \
    --render-scale 1 \
    --downsample-filter nearest
```

### Options

| Option | Default | Description |
|--------|---------|-------------|
| `--output` | `dataset` | Output directory for the dataset |
| `--per-class` | `250` | Number of images to generate per class |
| `--resume` | `False` | Skip images that already exist |
| `--render-scale` | `4` | Render at `OUTPUT_WIDTH × scale` × `OUTPUT_HEIGHT × scale` before downsampling. Higher values reduce aliasing but slow rendering roughly by `scale²`. |
| `--downsample-filter` | `lanczos` | PIL filter used when resizing the high-resolution render to the final output size. Choices: `lanczos`, `bilinear`, `bicubic`, `box`, `nearest`. |
| `--max-lat` | `45.0` | Maximum camera latitude variation from the equator, in degrees. |
| `--max-lon` | `30.0` | Maximum camera longitude offset around the planet's axis, in degrees. |

## Splitting the dataset

Use `split_dataset.py` to carve out a balanced set of images from a chosen set of classes and place them in per-class folders under `data/raw/`. The remaining images (unused images from the selected classes plus any withheld classes) go into `extra-data/extra/` for inference-time drift evaluation.

By default, inference filenames are kept as `<Class>_<N>.jpg` so you can inspect the split. Pass `--encode` to obfuscate them with reversed URL-safe base64:

```bash
python split_dataset.py \
    --input dataset \
    --output-data data/raw \
    --output-extra extra-data/extra \
    --train-classes Mercury Venus Earth Mars Jupiter Saturn Uranus Neptune Moon Pluto \
    --images-per-class 150 \
    --seed 42 \
    --encode
```

This produces:

```
dataset/
├── Mercury/
├── Venus/
├── Earth/
└── ... (14 classes, 150 images each)
data/
└── raw/
    ├── Earth/
    │   ├── Earth_3.jpg
    │   └── ... (150 images)
    ├── Mars/
    │   └── ... (150 images)
    └── ... (10 classes total)
extra-data/
└── extra/
    ├── <encoded>.jpg
    ├── <encoded>.jpg
    └── ...
```

Inference filenames are encoded with reversed URL-safe base64 (no padding). Reversing the encoded string moves the high-entropy part of the name to the front, so adjacent files in a sorted directory listing come from random categories and do not reveal the class.

To restore the original inference filenames, run:

```bash
python split_dataset.py --decode --decode-dir extra-data/extra
```

This renames files in place inside `extra-data/extra/` without moving them into subfolders or re-running the split.

### `split_dataset.py` options

| Option | Default | Description |
|--------|---------|-------------|
| `--input` | `dataset` | Full generated dataset directory |
| `--output-data` | `data` | Root directory for the per-class data folders (example: `data/raw`) |
| `--output-extra` | `extra-data/extra` | Directory for the obfuscated inference set |
| `--train-classes` | 8 planets + Moon + Pluto | Space-separated list of classes placed in `--output-data` |
| `--images-per-class` | `150` | Number of images sampled per class |
| `--seed` | `42` | Random seed for reproducible sampling |
| `--move` | `False` | Move inference images to `extra-data/extra/` instead of copying |
| `--overwrite` | `False` | Replace existing output directories |
| `--encode` | `False` | Encode inference filenames in `extra-data/extra/` with reversed base64 |
| `--decode` | `False` | Decode obfuscated inference filenames back to originals |
| `--decode-dir` | `extra-data/extra` | Directory to decode when `--decode` is used |

## Output

- Image size: `128 × 128` pixels
- Color mode: RGB
- Background: black
- File format: JPEG (quality 95)

## Notes

- Saturn is rendered with its rings locked to the equatorial plane. The ring opening and projection follow naturally from the randomized camera position.
- Haumea is rendered as a triaxial ellipsoid.
- All other bodies are rendered as spheres.
- Texture resolutions are down-sampled internally to a consistent equirectangular size, so the generator works with both 2K and 4K source maps.

## Texture sources and references

The texture maps used by the generators come from several public sources. When re-distributing or publishing work based on these images, please credit the original creators according to their respective licenses.

### Primary sources used

- **Solar System Scope** — high-resolution planet and fictional dwarf-planet textures.  
  <https://www.solarsystemscope.com/textures/>

- **CelestiaProject / CelestiaContent** — high-resolution moon textures (Europa, Ganymede, Callisto, Mimas, Enceladus, Tethys, Dione, Rhea, Iapetus, Hyperion, Phobos, Deimos, Triton, Charon) and data licensing information.  
  <https://github.com/CelestiaProject/CelestiaContent>

- **DeviantArt / Ducn1567** — Pluto texture.  
  <https://www.deviantart.com/ducn1567/gallery>  
  Direct piece: <https://www.deviantart.com/ducn1567/art/Pluto-Texture-2K-1014814564>

- **DeviantArt / 4stron4omi4 — Pluto Texture Map (Fixed Blur / Unmapped Areas)**  
  <https://www.deviantart.com/4stron4omi4/art/Pluto-Texture-Map-Fixed-Blur-Unmaped-Areas-1101489593>

- **Björn Jónsson planetary maps** — Io texture.  
  <https://bjj.mmedia.is/data/planetary_maps.html>

- **NASA Photojournal / PIA22770** — base grayscale Titan global mosaic used in the composite Titan texture.  
  <https://photojournal.jpl.nasa.gov/catalog/PIA22770>

### Additional reference resources consulted

- **NASA 3D Resources**  
  <https://science.nasa.gov/3d-resources/>

- **JPL Solar System Maps**  
  <https://maps.jpl.nasa.gov/tmaps/>

- **Celestia Motherlode**  
  <http://celestiamotherlode.net/catalog/solarsystem.html>

- **Planets and Moons Dataset — AI in Space**  
  <https://www.kaggle.com/datasets/emirhanai/planets-and-moons-dataset-ai-in-space>

