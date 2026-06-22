# Dataset

This branch is only intended to keep the Python script that generates a synthetic image dataset of planets, dwarf planets, and moons using the **SIMply** ray-tracing library.

The generator renders textured spheres (and Saturn's rings) from randomized camera angles and saves the images as `128 × 128` RGB JPEGs on a black background.

## What is generated

Each class gets a dedicated folder with `150` images named `<ClassName>_<N>.jpg`.

Example folder layout after generation:

```
datas/raw/
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
python venv .venv
```

### 3. Install Python packages

The generator assumes the required packages are already installed in the active environment. You can install them with:

```bash
pip install numpy pillow opencv-python scipy astropy open3d pandas matplotlib
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
    --output data/raw \
    --per-class 150
```

### Options

| Option | Default | Description |
|--------|---------|-------------|
| `--output` | `data/raw` | Output directory for the dataset |
| `--per-class` | `150` | Number of images to generate per class |
| `--resume` | `False` | Skip images that already exist |

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

