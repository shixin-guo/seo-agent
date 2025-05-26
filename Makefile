.PHONY: init lint format typecheck test mock clean

init:
	poetry install --with dev
	poetry run pre-commit install

lint:
	poetry run ruff check seo_agent main.py --extend-exclude tests/

format:
	poetry run ruff format seo_agent main.py
	poetry run ruff check --fix seo_agent main.py

typecheck:
	poetry run mypy seo_agent main.py

test:
	poetry run pytest

test-unit:
	poetry run pytest -m unit

test-integration:
	poetry run pytest -m integration

test-cov:
	poetry run pytest --cov=seo_agent --cov-report=term --cov-report=xml --cov-report=html



all: format lint typecheck test

clean:
	rm -rf __pycache__
	rm -rf .pytest_cache
	rm -rf .mypy_cache
	rm -rf .coverage
	rm -rf .ruff_cache
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name "*.egg" -exec rm -rf {} +
	find . -type d -name .ipynb_checkpoints -exec rm -rf {} +
