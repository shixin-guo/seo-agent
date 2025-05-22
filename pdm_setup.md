# Managing Python Dependencies with PDM

This guide explains how to use PDM to manage dependencies for the SEO Agent project.

## What is PDM?

PDM (Python Development Master) is a modern Python package and dependency manager supporting the latest PEP standards. It's designed to work with Python 3.7+, and is compatible with PEP 621 (project metadata in pyproject.toml).

## Installing PDM

### macOS (using Homebrew):
```bash
brew install pdm
```

### Using pip:
```bash
pip install --user pdm
```

### Other installation methods:
See [PDM Installation Guide](https://pdm.fming.dev/latest/#installation)

## Using PDM with SEO Agent

### 1. Initialize PDM in the Project
Navigate to the project directory and run:

```bash
cd /Users/ShixinGuo/code/seo-agent
pdm init
```

This will create a new `pyproject.toml` file or update an existing one. You can accept the defaults or configure as needed.

### 2. Install Dependencies

The project has already been configured to work with PDM in the `pyproject.toml` file. You can install dependencies immediately:

```bash
pdm install
```

To include development dependencies:

```bash
pdm install -G dev
```

### 3. Running Commands with PDM

To run the SEO Agent:

```bash
pdm run python -m seo_agent.main keyword-research --seed "digital marketing" --industry "saas"
```

### 4. Adding New Dependencies

```bash
# Add a regular dependency
pdm add numpy

# Add a development dependency
pdm add -G dev pytest
```

### 5. Removing Dependencies

```bash
pdm remove numpy
```

### 6. Updating Dependencies

```bash
# Update all dependencies
pdm update

# Update specific dependency
pdm update requests
```

### 7. Creating a Virtual Environment

PDM manages virtual environments internally, but you can also create them explicitly:

```bash
pdm venv create
```

To activate the environment:

```bash
eval $(pdm venv activate)
```

## Benefits of Using PDM

1. **PEP 621 Support**: Uses standardized Python project metadata.
2. **Fast**: PDM is designed to be faster than other package managers.
3. **Lockfile**: The `pdm.lock` file ensures consistent installations.
4. **Dependency Groups**: Organize dependencies into groups (like development, testing, etc.)
5. **PEP 582 Support**: Can use the `__pypackages__` directory for package installation.
6. **Plugin System**: Extensible with plugins.

## Using the Demo Mode with PDM

```bash
pdm run python simple_keyword_demo.py --seed "digital marketing" --industry "saas" --auto-csv
```

## GitHub Actions Integration

To use PDM in your GitHub Actions workflows, add this to your workflow file:

```yaml
- name: Set up PDM
  uses: pdm-project/setup-pdm@v3
  with:
    python-version: '3.11'

- name: Install dependencies
  run: pdm install -G dev

- name: Run linting
  run: pdm run make lint
```
