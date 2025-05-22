# Python Dependency Management Options for SEO Agent

This guide provides a comparison of different dependency management tools that can help you manage Python dependencies without manually handling virtual environments.

## Comparison of Options

| Feature | Poetry | PDM | Pipenv | Conda | pip-tools |
|---------|--------|-----|--------|-------|-----------|
| Ease of use | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ | ⭐⭐ |
| Lockfile | ✅ | ✅ | ✅ | ✅ | ✅ |
| Auto-venv management | ✅ | ✅ | ✅ | ✅ | ❌ |
| PEP 621 support | ✅ | ✅ | ❌ | ❌ | ❌ |
| Dependency resolution | ✅ | ✅ | ✅ | ✅ | ✅ |
| Dev dependencies | ✅ | ✅ | ✅ | ✅ | ✅ |
| Packaging | ✅ | ✅ | ❌ | ✅ | ❌ |
| Project scripts | ✅ | ✅ | ✅ | ✅ | ❌ |
| Community adoption | High | Medium | High | High | Medium |

## Recommended Options

### 1. Poetry (Recommended for most users)

Poetry provides a clean, modern approach to Python packaging. It's easy to use and handles everything from dependency management to building and publishing packages.

We have prepared the project for Poetry - see [poetry_setup.md](poetry_setup.md) for instructions.

**Quick Start**:
```bash
# Install Poetry
curl -sSL https://install.python-poetry.org | python3 -

# Install dependencies
cd /Users/ShixinGuo/code/seo-agent
poetry install

# Run the application
poetry run python -m seo_agent.main keyword-research --seed "digital marketing" --industry "saas"
```

### 2. PDM (Modern alternative to Poetry)

PDM is a newer tool that follows the latest PEP standards. It's similar to Poetry but has some unique features like PEP 582 support (which allows installing packages in a `__pypackages__` directory).

See [pdm_setup.md](pdm_setup.md) for detailed instructions.

**Quick Start**:
```bash
# Install PDM
pip install --user pdm

# Install dependencies
cd /Users/ShixinGuo/code/seo-agent
pdm install

# Run the application
pdm run python -m seo_agent.main keyword-research --seed "digital marketing" --industry "saas"
```

### 3. Pipenv (More traditional approach)

Pipenv combines pip and virtualenv into a single tool. It's more established and has been around longer than Poetry or PDM.

We have prepared a Pipfile for you - see [pipenv_setup.md](pipenv_setup.md) for instructions.

**Quick Start**:
```bash
# Install Pipenv
pip install --user pipenv

# Install dependencies
cd /Users/ShixinGuo/code/seo-agent
pipenv install

# Run the application
pipenv run python main.py keyword-research --seed "digital marketing" --industry "saas"
```

### 4. Conda (Good for data science projects)

Conda is particularly useful if you're working with data science libraries or need to manage non-Python dependencies.

```bash
# Install Miniconda
# (Visit https://docs.conda.io/en/latest/miniconda.html for installation instructions)

# Create a conda environment
conda create -n seo-agent python=3.11

# Activate the environment
conda activate seo-agent

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py keyword-research --seed "digital marketing" --industry "saas"
```

### 5. pip-tools (Lightweight approach)

pip-tools is a set of tools to keep your pinned dependencies up-to-date.

```bash
# Install pip-tools
pip install pip-tools

# Generate pinned requirements
pip-compile requirements.in

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py keyword-research --seed "digital marketing" --industry "saas"
```

## Recommendation

For the SEO Agent project, we recommend using **Poetry** because:

1. It provides a comprehensive solution for dependency management
2. It's well-documented and has strong community support
3. It automatically handles virtual environments
4. It uses modern Python packaging standards
5. It offers a clean workflow for development

Follow the instructions in [poetry_setup.md](poetry_setup.md) to get started with Poetry.
