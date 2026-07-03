# A guide to MLOps — Agent notes

Quick reference for AI coding agents working on the repository.

## Project overview

This repository is the source for the **"A guide to MLOps"** website at
<https://mlops.swiss-ai-center.ch> and its companion slide deck.

- It is a hands-on tutorial that takes a planet/moon image classifier from a
  Jupyter Notebook experiment to a reproducible, deployed, monitored, and
  retrainable ML system.
- The tutorial covers: Git, DVC, GitHub Actions, CML, BentoML, Docker,
  Kubernetes, Evidently AI, and Label Studio.
- The `main` branch contains the documentation and presentation source. Related
  artifacts live on dedicated branches:
  - `dataset` — dataset generator
  - `data` — dataset used for training/evaluation
  - `extra-data` — supplementary data for inference and labeling
  - `freeze` — backup of validated dependency pins

Key files:

- `README.md` — high-level description, branch layout, and local setup.
- `zensical.toml` — documentation site generator configuration.
- `pyproject.toml` — Python project metadata.
- `Dockerfile` / `docker-compose.yml` — containerized local development.
- `.github/workflows/deploy-to-github-pages.yml` — CI/CD and Pages deployment.

## Technology stack

- **Python 3.13** (minimum version, per `pyproject.toml`).
- **Zensical** — documentation site generator (Material for MkDocs-based).
- **mdwrap** — Markdown formatter/linter.
- **Marp CLI** — builds the presentation deck.
- **Docker / Docker Compose** — optional local dev environment.
- **GitHub Actions** — linting, building, and deploying to GitHub Pages.

Production dependencies are pinned in `requirements-freeze.txt`; direct
dependencies are listed in `requirements.txt`.

## Repository structure

```text
.
├── docs/                         # Guide Markdown source
│   ├── index.md                  # Story landing page
│   ├── syllabus.md               # Tutorial overview
│   ├── tools.md                  # Tooling overview
│   ├── cheatsheet.md             # Terminal/command reference
│   ├── philosophy.md
│   ├── concept.md
│   ├── references.md
│   ├── glossary.md
│   ├── clean-up.md
│   ├── conclusion.md
│   ├── part-1-local-training-and-evaluation/
│   ├── part-2-move-to-the-cloud/
│   ├── part-3-serve-and-deploy/
│   ├── part-4-monitor-and-maintain/
│   ├── part-5-label-data-and-retrain/
│   ├── assets/                   # Images, CSS, JavaScript
│   └── overrides/                # Jinja2 template overrides
├── presentation/                 # Marp slide deck
│   ├── README.md                 # Slide source
│   ├── images/                   # Slide assets
│   └── index.html                # Generated HTML deck
├── logs/                         # Empty by default; used by monitoring chapter
├── site/                         # Generated Zensical output (gitignored)
├── public/                       # Final GitHub Pages artifact (gitignored)
├── zensical.toml                 # Site generator configuration
├── pyproject.toml                # Python project metadata
├── requirements.txt              # Direct dependencies
├── requirements-freeze.txt       # Pinned dependencies used by CI/Docker
├── Dockerfile
├── docker-compose.yml
└── .github/workflows/deploy-to-github-pages.yml
```

## Build and serve

### Python

```sh
python3.13 -m venv .venv
source .venv/bin/activate
pip install -r requirements-freeze.txt
zensical serve
```

Open <http://localhost:8000>. The server reloads on documentation changes.

### uv

```sh
uv venv --python 3.13
source .venv/bin/activate
uv pip install -r requirements-freeze.txt
zensical serve
```

### Docker Compose

```sh
docker compose build
docker compose up serve
```

### Production build

```sh
zensical build --clean
```

This writes the static site to `site/`.

## Formatting and linting

The project uses `mdwrap` to keep Markdown consistent. CI validates formatting
and builds both the site and the presentation.

- Format:

  ```sh
  mdwrap --fmt docs presentation
  ```

- Check:

  ```sh
  mdwrap --check docs presentation
  ```

## CI/CD and deployment

`.github/workflows/deploy-to-github-pages.yml` runs on pushes to `main`, pull
requests, and `workflow_dispatch`. It lints with `mdwrap --check`, builds the
site with `zensical build --clean`, builds the presentation with Marp, merges
both artifacts into `public/`, and deploys `public/` to GitHub Pages from
`main`.

The live site is configured in `zensical.toml`:

- `site_url = "https://mlops.swiss-ai-center.ch/"`
- `repo_url = "https://github.com/swiss-ai-center/a-guide-to-mlops"`

## Development conventions

- Markdown files use **4-space indentation** (`.editorconfig`).
- Keep Markdown sources under `docs/` and `presentation/README.md` wrapped and
  formatted with `mdwrap`.
- The guide relies on Zensical/Material for MkDocs features configured in
  `zensical.toml`: admonitions, footnotes, content tabs, task lists, code
  annotations, Mermaid diagrams, emoji, and MathJax.
- Shell instructions use fenced code blocks with a title.
- Alternate tooling choices use content tabs.
- Navigation is explicit in `zensical.toml` (`nav` array), not derived from the
  directory structure.
- Custom templates live in `docs/overrides/`. `docs/index.md` renders with
  `docs/overrides/home.html`.

## Security and cost considerations

The guide instructs readers to create cloud resources (Google Cloud projects,
GitHub tokens, container registries, Kubernetes clusters, S3 buckets, etc.).
`docs/clean-up.md` explains how to remove them.

No credentials or secrets are stored in this repository.

## Useful references

- `README.md` — branch layout and quick setup.
- `zensical.toml` — site name, URL, navigation, theme, palette, and Markdown
  extensions.
- `.github/workflows/deploy-to-github-pages.yml` — full CI/CD pipeline.
- `docs/tools.md` — overview of the MLOps tools used in the tutorial.
- `docs/syllabus.md` — tutorial structure and chapter list.
