"""Generate a reduced planets-and-dwarfs dataset using SIMply.

Only includes the major planets and selected dwarf planets:
Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus, Neptune,
Moon, Ceres, Pluto, Eris, Haumea, Makemake.

Output filenames are ``<ClassName>_<N>.jpg``.

Output: dataset  (14 classes, 150 images each, 128x128 RGB)

Usage:
    python generate_planet_dataset_simply.py \
        --output dataset --per-class 150
"""

from __future__ import annotations

import argparse
import hashlib
import math
import random
import sys
import time
import warnings
from pathlib import Path
from typing import Callable

import numpy as np
from PIL import Image

# ---------------------------------------------------------------------------
# Locate SIMply source tree
# ---------------------------------------------------------------------------
SIMPLY_DIR = Path(__file__).resolve().parent / "simply"
if not SIMPLY_DIR.is_dir():
    raise FileNotFoundError(
        f"SIMply source tree not found at {SIMPLY_DIR}. "
        "Clone https://github.com/gbrydon/SIMply into the project root."
    )
sys.path.insert(0, str(SIMPLY_DIR))

from cameras.cameras import Camera  # noqa: E402
from coremaths.frame import Frame  # noqa: E402
from coremaths.geometry import Spheroid  # noqa: E402
from coremaths.vector import Vec3  # noqa: E402
from radiometry.reflectance_funcs import BRDF  # noqa: E402
from rendering.lights import Light  # noqa: E402
from rendering.meshes import Mesh  # noqa: E402
from rendering.renderables import RenderableObject, RenderableScene  # noqa: E402
from rendering.renderer import Renderer  # noqa: E402
from rendering.textures import Texture  # noqa: E402
from simply_utils.constants import au as AU_METERS  # noqa: E402

warnings.filterwarnings("ignore", category=RuntimeWarning)

# ---------------------------------------------------------------------------
# Image / scene settings
# ---------------------------------------------------------------------------
OUTPUT_WIDTH = 128
OUTPUT_HEIGHT = 128
TEXTURE_WIDTH = 2048
TEXTURE_HEIGHT = 1024

FOV_X = 50.0  # degrees, horizontal
FOV_Y = FOV_X * OUTPUT_HEIGHT / OUTPUT_WIDTH  # 50.0 degrees for 1:1 aspect ratio

# Render-scale for anti-aliasing.  The scene is rendered at
# OUTPUT_WIDTH*RENDER_SCALE x OUTPUT_HEIGHT*RENDER_SCALE and then downsampled
# to the final OUTPUT_WIDTH x OUTPUT_HEIGHT with a high-quality resampling
# filter.  RENDER_SCALE=4 means 16 rays are traced per output pixel, giving
# very smooth silhouettes against the black background.
RENDER_SCALE = 4

# Downsample filter used when resizing the high-resolution render to the final
# output size.  LANCZOS gives the sharpest, highest-quality result.  BILINEAR
# is slightly softer but cheaper and avoids any faint ringing on very high-
# contrast edges.
DOWNSAMPLE_FILTER = Image.Resampling.LANCZOS

# Camera distance chosen so the object fills ~78% of the shorter image axis,
# keeping margins small while ensuring the body stays fully inside the frame
# even with random camera latitude/longitude variations and renderer overshoot.
# For a sphere of radius R: distance = R / tan(0.78 * fov_y / 2)
FIT_FACTOR = 0.85
BASE_DISTANCE = 1.0 / math.tan(math.radians(FOV_Y * FIT_FACTOR / 2))

# Saturn's rings extend from ~1.2 to ~2.3 Saturn radii. We frame the outer edge.
SATURN_RING_OUTER = 2.35

# Haumea triaxial ellipsoid semi-axis ratios (Ortiz et al. 2017 occultation fit)
# a:b:c = 1161:852:513
HAUMEA_AXES = (1.0, 852 / 1161, 513 / 1161)

# Mesh resolution for the Haumea triaxial ellipsoid.  A denser mesh gives a
# smoother silhouette but slows rendering; 128x256 is a good trade-off for a
# 128x128 output with 4x supersampling.
HAUMEA_MESH_LAT = 128
HAUMEA_MESH_LON = 256

# Camera angle diversity defaults.  Latitude is the vertical tilt from the
# equator toward either pole; longitude is the azimuthal offset around the
# planet's axis, which adds subtle perspective variety.  Both can be overridden
# with --max-lat and --max-lon on the command line.
CAMERA_MAX_LAT = math.radians(45.0)
CAMERA_MAX_LON = math.radians(30.0)

# Light source distance.  The sun is placed 1 AU away along the randomly chosen
# light direction.  This only matters when physical radiance rendering is used
# (the texture-only path ignores the light entirely).
LIGHT_DISTANCE = AU_METERS

# Realistic Saturn ring opening angle range (degrees). Saturn's ring plane is
# inclined ~26.7 degrees to its orbital plane; the apparent opening angle
# varies from nearly 0 (edge-on) to about 27 degrees. We use 15-28 degrees.
SATURN_RING_OPENING_MIN = 15.0
SATURN_RING_OPENING_MAX = 28.0

# ---------------------------------------------------------------------------
# Texture loading
# ---------------------------------------------------------------------------
TEXTURE_DIR = Path(__file__).resolve().parent / "textures"


def _seed_int(seed: str | int) -> int:
    if isinstance(seed, int):
        return seed & 0xFFFFFFFF
    return int(hashlib.sha256(str(seed).encode()).hexdigest()[:8], 16) & 0xFFFFFFFF


def load_texture(name: str) -> np.ndarray:
    """Load a texture image and return it as a uint8 RGB numpy array."""
    path = TEXTURE_DIR / name
    img = Image.open(path).convert("RGB")
    # Resize to a consistent high-res equirectangular size
    img = img.resize((TEXTURE_WIDTH, TEXTURE_HEIGHT), Image.Resampling.LANCZOS)
    return np.array(img)


def earth_texture(seed: int) -> np.ndarray:
    """Combine Solar System Scope day map and cloud map."""
    day = load_texture("2k_earth_daymap.jpg")
    clouds = load_texture("2k_earth_clouds.jpg")
    # Cloud texture is grayscale-ish; use its brightness as alpha
    cloud_alpha = (clouds.mean(axis=2, keepdims=True) / 255.0) * 0.80
    tex = day * (1.0 - cloud_alpha) + clouds * cloud_alpha
    return np.clip(tex, 0, 255).astype(np.uint8)


def load_or_generate(name: str, seed: int) -> Callable[[int], np.ndarray]:
    """Return a function that produces the texture for a given seed."""
    mapping = {
        "Mercury": lambda s: load_texture("2k_mercury.jpg"),
        "Venus": lambda s: load_texture("2k_venus_atmosphere.jpg"),
        "Earth": earth_texture,
        "Mars": lambda s: load_texture("2k_mars.jpg"),
        "Jupiter": lambda s: load_texture("2k_jupiter.jpg"),
        "Saturn": lambda s: load_texture("2k_saturn.jpg"),
        "Uranus": lambda s: load_texture("2k_uranus.jpg"),
        "Neptune": lambda s: load_texture("2k_neptune.jpg"),
        "Moon": lambda s: load_texture("2k_moon.jpg"),
        "Pluto": lambda s: load_texture("2k_pluto.jpg"),
        "Ceres": lambda s: load_texture("2k_ceres_fictional.jpg"),
        "Eris": lambda s: load_texture("2k_eris_fictional.jpg"),
        "Haumea": lambda s: load_texture("2k_haumea_fictional.jpg"),
        "Makemake": lambda s: load_texture("2k_makemake_fictional.jpg"),
    }
    return mapping[name]


PLANET_NAMES = [
    "Mercury", "Venus", "Earth", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune",
    "Moon", "Pluto", "Ceres", "Eris", "Haumea", "Makemake",
]


# ---------------------------------------------------------------------------
# Saturn ring mesh and texture
# ---------------------------------------------------------------------------


def create_saturn_ring_mesh(
    frame: Frame | None = None,
    inner: float = 1.25,
    outer: float = SATURN_RING_OUTER,
    n_radial: int = 256,
    n_angular: int = 256,
    alpha_texture: np.ndarray | None = None,
    alpha_threshold: int = 8,
) -> Mesh:
    """Create an annular ring mesh in the y-z plane, optionally transformed by ``frame``.

    If ``alpha_texture`` is supplied, radial segments whose average alpha is below
    ``alpha_threshold`` are omitted, creating physical gaps through which the
    planet (or background) is visible.
    """
    radii = np.linspace(inner, outer, n_radial)
    thetas = np.linspace(0, 2 * math.pi, n_angular, endpoint=False)
    verts = []
    uvs = []
    for r in radii:
        for t in thetas:
            verts.append([0.0, r * math.cos(t), r * math.sin(t)])
            uvs.append([(r - inner) / (outer - inner), t / (2 * math.pi)])
    verts = np.array(verts, dtype=np.float32)
    uvs = np.array(uvs, dtype=np.float32)

    # Pre-compute which radial segments have enough ring material to keep.
    keep_segment = np.ones(n_radial - 1, dtype=bool)
    if alpha_texture is not None:
        alpha_h, alpha_w = alpha_texture.shape[:2]
        for i in range(n_radial - 1):
            u_start = (radii[i] - inner) / (outer - inner)
            u_end = (radii[i + 1] - inner) / (outer - inner)
            c0 = int(np.clip(u_start * alpha_w, 0, alpha_w - 1))
            c1 = int(np.clip(u_end * alpha_w, 0, alpha_w - 1))
            if c1 <= c0:
                c1 = c0 + 1
            segment_alpha = alpha_texture[:, c0:c1].mean()
            keep_segment[i] = segment_alpha >= alpha_threshold

    tris = []
    for i in range(n_radial - 1):
        if not keep_segment[i]:
            continue
        for j in range(n_angular):
            j_next = (j + 1) % n_angular
            v0 = i * n_angular + j
            v1 = i * n_angular + j_next
            v2 = (i + 1) * n_angular + j_next
            v3 = (i + 1) * n_angular + j
            tris.append([v0, v1, v2])
            tris.append([v0, v2, v3])
    tris = np.array(tris, dtype=np.int32)

    mesh = Mesh(verts, tris, frame=frame)
    mesh.textureCoordArray = uvs
    mesh.triTexIndices = tris
    return mesh


def create_saturn_ring_texture(size: tuple[int, int] = (4096, 128)) -> np.ndarray:
    """Create a radial Saturn ring texture with bright rings and dark gaps."""
    w, h = size
    tex = np.zeros((h, w, 3), dtype=np.uint8)
    x = np.linspace(0, 1, w)
    rng = np.random.default_rng(42)

    # Base radial profile (approximate Saturn ring structure)
    profile = np.full(w, 0.02)
    # D ring / inner C ring
    profile[(x > 0.03) & (x < 0.12)] = 0.18
    # C ring
    profile[(x > 0.13) & (x < 0.30)] = 0.55
    # B ring (brightest)
    profile[(x > 0.31) & (x < 0.55)] = 0.92
    # Cassini division (dark)
    profile[(x > 0.55) & (x < 0.59)] = 0.04
    # A ring
    profile[(x > 0.60) & (x < 0.92)] = 0.65
    # F ring / outer
    profile[(x > 0.93) & (x < 0.98)] = 0.35

    # Subtle radial banding/noise
    banding = np.sin(x * 80) * 0.03 + np.sin(x * 200) * 0.015
    noise = (rng.random(w) - 0.5) * 0.04
    profile = np.clip(profile + banding + noise, 0, 1)

    # Saturn ring colour: dusty tan / grey-white
    colour = np.array([205, 190, 165], dtype=np.float32)
    for i in range(h):
        tex[i, :, :] = (profile[:, None] * colour[None, :]).astype(np.uint8)
    return tex


def load_saturn_ring_textures() -> tuple[np.ndarray, np.ndarray]:
    """Load the real Saturn ring texture with alpha.

    Returns a (rgb, alpha) pair. If the RGBA file is missing, falls back to the
    procedural ring texture and a fully-opaque alpha channel.
    """
    path = TEXTURE_DIR / "2k_saturn_ring_alpha.png"
    if path.exists():
        img = Image.open(path).convert("RGBA")
        arr = np.array(img)
        return arr[:, :, :3], arr[:, :, 3]
    rgb = create_saturn_ring_texture()
    alpha = np.full(rgb.shape[:2], 255, dtype=np.uint8)
    return rgb, alpha


SATURN_RING_RGB, SATURN_RING_ALPHA = load_saturn_ring_textures()
SATURN_RING_TEXTURE = Texture(SATURN_RING_RGB)
SATURN_RING_ALPHA_TEXTURE = Texture(SATURN_RING_ALPHA)


# ---------------------------------------------------------------------------
# Haumea triaxial ellipsoid mesh
# ---------------------------------------------------------------------------


def create_haumea_mesh(
    a: float = HAUMEA_AXES[0],
    b: float = HAUMEA_AXES[1],
    c: float = HAUMEA_AXES[2],
    n_lat: int = HAUMEA_MESH_LAT,
    n_lon: int = HAUMEA_MESH_LON,
    frame: Frame | None = None,
) -> Mesh:
    """Create a triaxial ellipsoid mesh with equirectangular UV mapping.

    The mesh is parametrised by latitude ``phi`` (-pi/2 at the south pole,
    +pi/2 at the north pole) and longitude ``theta`` (0 at +x, increasing
    toward +y).  Texture coordinates match SIMply's planetocentric convention:
    ``u = theta / (2*pi)`` and ``v = 0.5 - phi/pi`` so that the texture's top
    row maps to the north pole (+z).

    Using a mesh instead of SIMply's analytic ``Spheroid`` gives full control
    over the UV parametrisation and lets Haumea be rotated to any 3-D
    orientation while the texture follows the surface correctly.
    """
    phis = np.linspace(-math.pi / 2, math.pi / 2, n_lat)
    thetas = np.linspace(0, 2 * math.pi, n_lon, endpoint=False)

    verts = []
    uvs = []
    for phi in phis:
        cos_phi = math.cos(phi)
        sin_phi = math.sin(phi)
        for theta in thetas:
            cos_theta = math.cos(theta)
            sin_theta = math.sin(theta)
            x = a * cos_phi * cos_theta
            y = b * cos_phi * sin_theta
            z = c * sin_phi
            verts.append([x, y, z])
            u = theta / (2 * math.pi)
            v = 0.5 - phi / math.pi
            uvs.append([u, v])

    verts = np.array(verts, dtype=np.float32)
    uvs = np.array(uvs, dtype=np.float32)

    tris = []
    for i in range(n_lat - 1):
        for j in range(n_lon):
            j_next = (j + 1) % n_lon
            v0 = i * n_lon + j
            v1 = i * n_lon + j_next
            v2 = (i + 1) * n_lon + j_next
            v3 = (i + 1) * n_lon + j
            tris.append([v0, v1, v2])
            tris.append([v0, v2, v3])

    tris = np.array(tris, dtype=np.int32)
    mesh = Mesh(verts, tris, frame=frame)
    mesh.textureCoordArray = uvs
    mesh.triTexIndices = tris
    return mesh


# ---------------------------------------------------------------------------
# Rendering helpers
# ---------------------------------------------------------------------------


def random_light_direction(rng: random.Random) -> Vec3:
    """Return a normalised light direction, mostly from the front/upper-left."""
    theta = rng.uniform(math.pi * 0.25, math.pi * 0.55)
    phi = rng.uniform(math.pi * 0.10, math.pi * 0.35)
    x = math.sin(theta) * math.cos(phi)
    y = -math.sin(phi)
    z = math.cos(theta) * math.sin(phi)
    return Vec3((x, y, z)).norm


def render_scene(
    scene: RenderableScene,
    camera: Camera,
    render_scale: int = RENDER_SCALE,
    downsample_filter: Image.Resampling = DOWNSAMPLE_FILTER,
    shade_scene: RenderableScene | None = None,
) -> np.ndarray:
    """Render an RGB image of the scene.

    By default the scene is rendered using only the texture (no shading or
    shadows).  If ``shade_scene`` is provided, a physically-based radiance
    render of that white-material scene is used as a shading mask, giving
    Lambertian diffuse shading and self-shadowing (e.g. Saturn's rings casting
    shadows on the planet).

    The scene is rendered at ``OUTPUT_WIDTH*render_scale`` by
    ``OUTPUT_HEIGHT*render_scale`` and then downsampled to the final output
    size using ``downsample_filter``.  Rendering at higher resolution and
    resampling smooths the jagged silhouette produced by one-ray-per-pixel
    rendering.
    """
    # Create a higher-resolution camera with the same field of view and pose.
    hires_camera = Camera.pinhole(
        (math.degrees(camera.fov[0]), math.degrees(camera.fov[1])),
        OUTPUT_WIDTH * render_scale,
        OUTPUT_HEIGHT * render_scale,
    )
    hires_camera.frame = camera.frame

    tex_img = Renderer.texture(scene, hires_camera, sf=1, nanv=(0, 0, 0), chan='rgb')

    if shade_scene is not None:
        # Render a white-Lambertian radiance image to obtain the diffuse shading
        # and shadow pattern.  The mask is normalised by its brightest non-zero
        # value so each image is auto-exposed.
        shade_img = Renderer.radiance(
            shade_scene, hires_camera, (400, 700), sf=1, n_shad=1
        )
        shade_img = np.nan_to_num(shade_img, nan=0.0, posinf=0.0, neginf=0.0)
        shade_max = shade_img.max()
        if shade_max > 0:
            shade_mask = np.clip(shade_img / shade_max, 0.0, 1.0)
        else:
            shade_mask = shade_img
        tex_img = tex_img * shade_mask[..., None]

    img = Image.fromarray(np.clip(tex_img, 0, 255).astype(np.uint8), mode='RGB')
    img = img.resize((OUTPUT_WIDTH, OUTPUT_HEIGHT), downsample_filter)
    return np.array(img)


def center_body_in_image(img_array: np.ndarray, threshold: int = 10) -> np.ndarray:
    """Translate the image so the body's bounding box is centred in the frame.

    For perspective views of a non-spherical body the silhouette can be
    slightly off-centre even though the 3-D body is at the origin.  This
    function shifts the rendered image so the bounding box of non-background
    pixels is centred, matching the framing of the spherical planets.
    """
    img = Image.fromarray(img_array, mode="RGB")
    gray = np.array(img.convert("L"))
    mask = gray > threshold
    ys, xs = np.where(mask)
    if len(xs) == 0:
        return img_array

    cx = (xs.min() + xs.max()) // 2
    cy = (ys.min() + ys.max()) // 2
    dx = (img.width // 2) - cx
    dy = (img.height // 2) - cy

    # Pure integer translation: nearest-neighbour resampling is exact.
    # Note the minus signs: PIL's AFFINE maps output coordinates to source
    # coordinates, so the translation in the matrix is the negative of the
    # desired image shift.
    centered = img.transform(
        img.size,
        Image.Transform.AFFINE,
        (1, 0, -dx, 0, 1, -dy),
        resample=Image.Resampling.NEAREST,
        fill=0,
    )
    return np.array(centered)


def build_camera(
    distance: float,
    rng: random.Random | None = None,
    max_lat: float | None = None,
    max_lon: float | None = None,
    force_lon_zero: bool = False,
) -> Camera:
    """Build a camera looking at the origin with north (+z) at the image top.

    If ``rng`` is supplied, the camera is placed at a random latitude up to
    ``max_lat`` (default ``CAMERA_MAX_LAT``) and a random longitude up to
    ``max_lon`` (default ``CAMERA_MAX_LON``) so the dataset includes more polar
    and perspective diversity. Set ``force_lon_zero`` to keep the camera in the
    x-z plane.
    """
    camera = Camera.pinhole((FOV_X, FOV_Y), OUTPUT_WIDTH, OUTPUT_HEIGHT)

    if rng is None:
        lat = 0.0
        lon = 0.0
    else:
        lat_max = CAMERA_MAX_LAT if max_lat is None else max_lat
        lon_max = CAMERA_MAX_LON if max_lon is None else max_lon
        lat = rng.uniform(-lat_max, lat_max)
        lon = 0.0 if force_lon_zero else rng.uniform(-lon_max, lon_max)

    # Spherical camera position (origin is at the planet centre).
    cos_lat = math.cos(lat)
    origin = Vec3((
        distance * cos_lat * math.cos(lon),
        distance * cos_lat * math.sin(lon),
        distance * math.sin(lat),
    ))

    # Look toward the origin.
    w = (-origin).norm

    # Keep the planet's north pole (+z) pointing toward the top of the image.
    # Image top is -v, so v points toward the projection of -z onto the image plane.
    # Near the poles the projection vanishes, so fall back to the world y-axis to
    # keep the camera frame well-defined.
    z_world = Vec3((0, 0, 1))
    north_proj = z_world - z_world.dot(w) * w
    if north_proj.dot(north_proj) < 1e-12:
        north_proj = Vec3((0, 1, 0)) - Vec3((0, 1, 0)).dot(w) * w
    north_proj = north_proj.norm
    v = -north_proj
    u = v.cross(w).norm

    camera.frame = Frame(u, v, w, origin)
    return camera


# ---------------------------------------------------------------------------
# Per-class rendering
# ---------------------------------------------------------------------------


def render_normal(
    texture: np.ndarray,
    light_dir: Vec3,
    distance: float,
    rng: random.Random,
    render_scale: int = RENDER_SCALE,
    downsample_filter: Image.Resampling = DOWNSAMPLE_FILTER,
    max_lat: float | None = None,
    max_lon: float | None = None,
    shaded: bool = False,
) -> np.ndarray:
    """Render a textured sphere centred in the frame."""
    sphere = Spheroid(Frame.world(), 1.0, 1.0, 1.0)
    brdf = BRDF.lambert(0.01)
    planet = RenderableObject.renderablePrimitive(sphere, brdf, Texture(texture))
    scene = RenderableScene([planet], Light.sunPointSource(LIGHT_DISTANCE * light_dir))
    camera = build_camera(distance, rng, max_lat=max_lat, max_lon=max_lon)

    shade_scene = None
    if shaded:
        white_planet = RenderableObject.renderablePrimitive(sphere, BRDF.lambert(1.0))
        shade_scene = RenderableScene([white_planet], Light.sunPointSource(LIGHT_DISTANCE * light_dir))

    return render_scene(
        scene, camera,
        render_scale=render_scale, downsample_filter=downsample_filter,
        shade_scene=shade_scene,
    )


def render_haumea(
    texture: np.ndarray,
    light_dir: Vec3,
    distance: float,
    rng: random.Random,
    render_scale: int = RENDER_SCALE,
    downsample_filter: Image.Resampling = DOWNSAMPLE_FILTER,
    max_lat: float | None = None,
    max_lon: float | None = None,
    shaded: bool = False,
) -> np.ndarray:
    """Render Haumea as a randomly oriented triaxial ellipsoid.

    Instead of SIMply's analytic ``Spheroid`` primitive, a triaxial ellipsoid
    mesh is built with equirectangular UVs and rotated to a uniformly random
    3-D orientation.  The camera is allowed to orbit a full 360 degrees in
    longitude, so the silhouette changes realistically with viewing angle: the
    long axis can be seen side-on (very elongated), end-on (more compact), or
    anywhere in between.
    """
    # Random 3-D orientation: pick a uniformly distributed rotation axis and
    # a random rotation angle.  This lets the long, medium and short axes point
    # toward the camera in any combination.
    u1, u2 = rng.random(), rng.random()
    theta = 2 * math.pi * u1
    phi = math.acos(2 * u2 - 1)
    axis = Vec3((math.sin(phi) * math.cos(theta), math.sin(phi) * math.sin(theta), math.cos(phi)))
    angle = rng.uniform(0, 2 * math.pi)
    frame = Frame.world().rotated(Vec3.zero(), axis, angle)

    mesh = create_haumea_mesh(frame=frame)
    brdf = BRDF.lambert(0.01)
    planet = RenderableObject.renderableMesh(mesh, brdf, Texture(texture))
    scene = RenderableScene([planet], Light.sunPointSource(LIGHT_DISTANCE * light_dir))
    # Allow the camera to orbit all the way around Haumea so the changing
    # projected shape is visible.  Latitude is still configurable; longitude is
    # always full 360° for this body.
    camera = build_camera(distance, rng, max_lat=max_lat, max_lon=math.pi)

    shade_scene = None
    if shaded:
        white_planet = RenderableObject.renderableMesh(mesh, BRDF.lambert(1.0))
        shade_scene = RenderableScene([white_planet], Light.sunPointSource(LIGHT_DISTANCE * light_dir))

    img = render_scene(
        scene, camera,
        render_scale=render_scale, downsample_filter=downsample_filter,
        shade_scene=shade_scene,
    )
    # Perspective views of the triaxial ellipsoid can shift the silhouette off
    # centre even though the 3-D body is at the origin.  Re-centre to match the
    # framing of the spherical planets.
    return center_body_in_image(img)


def render_saturn(
    texture: np.ndarray,
    light_dir: Vec3,
    distance: float,
    rng: random.Random,
    render_scale: int = RENDER_SCALE,
    downsample_filter: Image.Resampling = DOWNSAMPLE_FILTER,
    max_lat: float | None = None,
    max_lon: float | None = None,
    shaded: bool = False,
) -> np.ndarray:
    """Render Saturn with its rings locked to the equatorial plane.

    Saturn's rings lie in its equatorial plane (the world x-y plane). As the
    camera moves in latitude and longitude, the rings project naturally: their
    apparent opening angle and in-image rotation follow from the viewing
    geometry instead of being forced horizontal.
    """
    # Saturn oblate spheroid (slightly flattened)
    flattening = 0.90
    sphere = Spheroid(Frame.world(), 1.0, 1.0, flattening)
    brdf = BRDF.lambert(0.01)
    planet = RenderableObject.renderablePrimitive(sphere, brdf, Texture(texture))

    # Use the same camera variation as the other planets.
    camera = build_camera(distance, rng, max_lat=max_lat, max_lon=max_lon)

    # Ring mesh is built in the local y-z plane (normal local x). Lock that
    # plane to the world x-y plane (Saturn's equator):
    #   local x (normal) -> world +z
    #   local y          -> world +x
    #   local z          -> world +y
    ring_frame = Frame(Vec3((0, 0, 1)), Vec3((1, 0, 0)), Vec3((0, 1, 0)), Vec3.zero())
    ring_mesh = create_saturn_ring_mesh(
        frame=ring_frame,
        n_radial=256,
        alpha_texture=SATURN_RING_ALPHA,
        alpha_threshold=8,
    )
    ring = RenderableObject.renderableMesh(ring_mesh, BRDF.lambert(0.015), SATURN_RING_TEXTURE)

    scene = RenderableScene([planet, ring], Light.sunPointSource(LIGHT_DISTANCE * light_dir))

    shade_scene = None
    if shaded:
        white_planet = RenderableObject.renderablePrimitive(sphere, BRDF.lambert(1.0))
        # Re-use the same ring geometry (alpha culling) with a white BRDF so
        # the mask captures ring shadows on the planet.
        white_ring = RenderableObject.renderableMesh(ring_mesh, BRDF.lambert(1.0), SATURN_RING_TEXTURE)
        shade_scene = RenderableScene(
            [white_planet, white_ring],
            Light.sunPointSource(LIGHT_DISTANCE * light_dir),
        )

    return render_scene(
        scene, camera,
        render_scale=render_scale, downsample_filter=downsample_filter,
        shade_scene=shade_scene,
    )


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------


def generate_dataset(
    output_dir: str | Path,
    images_per_class: int = 150,
    resume: bool = False,
    render_scale: int = RENDER_SCALE,
    downsample_filter: Image.Resampling = DOWNSAMPLE_FILTER,
    max_lat: float | None = None,
    max_lon: float | None = None,
    shaded: bool = False,
) -> None:
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    total = len(PLANET_NAMES) * images_per_class
    count = 0
    skipped = 0
    start = time.time()

    # Pre-load/generate base textures once per class
    textures: dict[str, np.ndarray] = {}
    for name in PLANET_NAMES:
        tex_fn = load_or_generate(name, 0)
        textures[name] = tex_fn(0)

    for planet_name in PLANET_NAMES:
        class_dir = output_dir / planet_name
        class_dir.mkdir(parents=True, exist_ok=True)

        base_texture = textures[planet_name]

        # Distance chosen to fit the content vertically
        if planet_name == "Saturn":
            distance = BASE_DISTANCE * SATURN_RING_OUTER
        else:
            distance = BASE_DISTANCE

        for i in range(1, images_per_class + 1):
            out_path = class_dir / f"{planet_name}_{i - 1}.jpg"
            if resume and out_path.exists():
                skipped += 1
                count += 1
                continue

            seed = _seed_int(f"{planet_name}_simply13_{i}")
            rng = random.Random(seed)

            # Spin spherical planets around their north-south axis for variation.
            # Haumea uses the mesh's 3-D rotation instead, so its texture is kept
            # fixed relative to the body.
            if planet_name == "Haumea":
                texture = base_texture
            else:
                shift = rng.randint(0, TEXTURE_WIDTH - 1)
                texture = np.roll(base_texture, shift, axis=1)

            # Keep the camera distance fixed so the body stays centered and
            # consistently framed; only spin and lighting vary per image.
            dist = distance
            light_dir = random_light_direction(rng)

            if planet_name == "Haumea":
                img_array = render_haumea(
                    texture, light_dir, dist, rng,
                    render_scale=render_scale, downsample_filter=downsample_filter,
                    max_lat=max_lat, max_lon=max_lon, shaded=shaded,
                )
            elif planet_name == "Saturn":
                img_array = render_saturn(
                    texture, light_dir, dist, rng,
                    render_scale=render_scale, downsample_filter=downsample_filter,
                    max_lat=max_lat, max_lon=max_lon, shaded=shaded,
                )
            else:
                img_array = render_normal(
                    texture, light_dir, dist, rng,
                    render_scale=render_scale, downsample_filter=downsample_filter,
                    max_lat=max_lat, max_lon=max_lon, shaded=shaded,
                )

            img = Image.fromarray(img_array, mode="RGB")
            img.save(out_path, quality=95)

            count += 1
            if count % 100 == 0:
                elapsed = time.time() - start
                rate = count / elapsed
                remaining = (total - count) / rate if rate > 0 else 0
                print(f"Generated {count}/{total} images ({rate:.1f}/s, ~{remaining:.0f}s remaining)")

    elapsed = time.time() - start
    print(f"Done. Dataset written to {output_dir.resolve()} "
          f"({count - skipped} new images, {skipped} skipped, {elapsed:.1f}s).")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate improved SIMply planet dataset.")
    parser.add_argument("--output", type=str, default="dataset", help="Output directory")
    parser.add_argument("--per-class", type=int, default=150, help="Images per class")
    parser.add_argument("--resume", action="store_true", help="Skip images that already exist")
    parser.add_argument(
        "--render-scale",
        type=int,
        default=RENDER_SCALE,
        help="Render at OUTPUT_WIDTH*scale x OUTPUT_HEIGHT*scale and downsample. Default 4 (16 rays per output pixel).",
    )
    parser.add_argument(
        "--downsample-filter",
        type=str,
        choices=["lanczos", "bilinear", "bicubic", "box", "nearest"],
        default="lanczos",
        help="PIL filter used to resize the high-resolution render to the final size.",
    )
    parser.add_argument(
        "--max-lat",
        type=float,
        default=45.0,
        help="Maximum camera latitude variation in degrees (default: 45).",
    )
    parser.add_argument(
        "--max-lon",
        type=float,
        default=30.0,
        help="Maximum camera longitude offset in degrees (default: 30).",
    )
    parser.add_argument(
        "--shaded",
        action="store_true",
        help="Apply Lambertian diffuse shading and self-shadowing via a radiance render.",
    )
    args = parser.parse_args()
    filter_map = {
        "lanczos": Image.Resampling.LANCZOS,
        "bilinear": Image.Resampling.BILINEAR,
        "bicubic": Image.Resampling.BICUBIC,
        "box": Image.Resampling.BOX,
        "nearest": Image.Resampling.NEAREST,
    }
    generate_dataset(
        args.output,
        args.per_class,
        args.resume,
        render_scale=args.render_scale,
        downsample_filter=filter_map[args.downsample_filter],
        max_lat=math.radians(args.max_lat),
        max_lon=math.radians(args.max_lon),
        shaded=args.shaded,
    )
