# Managing Python Dependencies with Pipenv

This guide explains how to use Pipenv to manage dependencies for the SEO Agent project.

## What is Pipenv?

Pipenv is a dependency manager for Python projects that combines pip and virtualenv into a single tool. It automatically creates and manages a virtualenv for your projects, as well as adds/removes packages from your Pipfile as you install/uninstall packages.

## Installing Pipenv

### macOS (using Homebrew):
```bash
brew install pipenv
```

### Using pip:
```bash
pip install --user pipenv
```

## Using Pipenv with SEO Agent

### 1. Initialize Pipenv in the Project
Navigate to the project directory and run:

```bash
cd /Users/ShixinGuo/code/seo-agent
pipenv --python 3.11
```

This will create a new virtual environment and a `Pipfile`.

### 2. Install Dependencies

Install the dependencies from the requirements files:

```bash
# Install regular dependencies
pipenv install -r requirements.txt

# Install development dependencies
pipenv install -r requirements-dev.txt --dev
```

### 3. Running Commands with Pipenv

To run the SEO Agent:

```bash
pipenv run python main.py keyword-research --seed "digital marketing" --industry "saas"
```

Or enter a shell within the Pipenv virtual environment:

```bash
pipenv shell
python main.py keyword-research --seed "digital marketing" --industry "saas"
```

### 4. Adding New Dependencies

```bash
# Add a regular dependency
pipenv install numpy

# Add a development dependency
pipenv install pytest --dev
```

### 5. Removing Dependencies

```bash
pipenv uninstall numpy
```

### 6. Updating Dependencies

```bash
# Update all dependencies
pipenv update

# Update specific dependency
pipenv update requests
```

### 7. Generating requirements.txt

If you need to generate a requirements.txt file from your Pipfile:

```bash
pipenv lock -r > requirements.txt
pipenv lock -r --dev > requirements-dev.txt
```

## Benefits of Using Pipenv

1. **Simplified Workflow**: Combines pip and virtualenv into one tool.
2. **Automatic Environment Management**: Creates and manages virtual environments for you.
3. **Lockfile**: The `Pipfile.lock` ensures consistent installations.
4. **Deterministic Builds**: Ensures that your builds are deterministic and your deployments work.
5. **Security Features**: Checks for security vulnerabilities in your dependencies.

## Using the Demo Mode with Pipenv

```bash
pipenv run python simple_keyword_demo.py --seed "digital marketing" --industry "saas" --auto-csv
```

## GitHub Actions Integration

To use Pipenv in your GitHub Actions workflows, add this to your workflow file:

```yaml
- name: Set up Python
  uses: actions/setup-python@v4
  with:
    python-version: '3.11'

- name: Install pipenv
  run: pip install pipenv

- name: Install dependencies
  run: |
    pipenv install -r requirements.txt
    pipenv install -r requirements-dev.txt --dev

- name: Run linting
  run: pipenv run make lint
```
