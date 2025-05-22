.PHONY: init lint format typecheck test clean

init:
	pip install -r requirements-dev.txt
	pre-commit install

lint:
	flake8 seo_agent main.py

format:
	black seo_agent main.py
	isort seo_agent main.py

typecheck:
	mypy seo_agent main.py

test:
	# Add testing command here when tests are implemented
	echo "No tests implemented yet"

all: format lint typecheck test

clean:
	rm -rf __pycache__
	rm -rf .pytest_cache
	rm -rf .mypy_cache
	rm -rf .coverage
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name "*.egg" -exec rm -rf {} +
	find . -type d -name .ipynb_checkpoints -exec rm -rf {} +
