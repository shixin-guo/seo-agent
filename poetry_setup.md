# Managing Python Dependencies with Poetry

This guide explains how to use Poetry to manage dependencies for the SEO Agent project.

## What is Poetry?

Poetry is a tool for dependency management and packaging in Python. It allows you to declare the libraries your project depends on and it will manage (install/update) them for you. Poetry offers a lockfile to ensure repeatable installations, and can build your project for distribution.

## Installing Poetry

### macOS/Linux/WSL:
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

### Windows (PowerShell):
```powershell
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -
```

## Using Poetry with SEO Agent

### 1. Initialize Poetry in the Project
Navigate to the project directory and run:

```bash
cd /Users/ShixinGuo/code/seo-agent
poetry init
```

This will create a new `pyproject.toml` file. You can accept the defaults or configure as needed.

### 2. Convert to Poetry

The project has already been converted to use Poetry format in the `pyproject.toml` file. You can start using it right away.

### 3. Install Dependencies

```bash
poetry install
```

This will create a virtual environment and install all dependencies specified in the pyproject.toml file.

To include development dependencies:

```bash
poetry install --with dev
```

### 4. Running Commands in the Poetry Environment

To run the SEO Agent:

```bash
poetry run python -m seo_agent.main keyword-research --seed "digital marketing" --industry "saas"
```

Or enter a shell within the Poetry virtual environment:

```bash
poetry shell
python -m seo_agent.main keyword-research --seed "digital marketing" --industry "saas"
```

### 5. Adding New Dependencies

```bash
# Add a regular dependency
poetry add numpy

# Add a development dependency
poetry add --group dev pytest
```

### 6. Removing Dependencies

```bash
poetry remove numpy
```

### 7. Updating Dependencies

```bash
# Update all dependencies
poetry update

# Update specific dependency
poetry update requests
```

## Benefits of Using Poetry

1. **Automatic Virtual Environment Management**: Poetry creates and manages virtual environments for you.
2. **Dependency Resolution**: Poetry resolves dependencies and their versions automatically.
3. **Lockfile**: The `poetry.lock` file ensures that the same dependencies are installed every time.
4. **Simplified Packaging**: Poetry can build and publish your project to PyPI.
5. **Dev Dependencies**: Separate dependencies for development vs. production.

## Using the Demo Mode with Poetry

```bash
poetry run python simple_keyword_demo.py --seed "digital marketing" --industry "saas" --auto-csv
```

## GitHub Actions Integration

To use Poetry in your GitHub Actions workflows, add this to your workflow file:

```yaml
- name: Set up Poetry
  uses: snok/install-poetry@v1
  with:
    version: 1.5.1
    virtualenvs-create: true
    virtualenvs-in-project: true

- name: Install dependencies
  run: poetry install --with dev

- name: Run linting
  run: poetry run make lint
```
