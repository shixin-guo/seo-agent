.PHONY: init lint format typecheck test mock clean docs docs-check

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

docs:
	python scripts/build_llm_docs.py

docs-check: docs
	@echo "Checking generated documentation files..."
	@test -f llm.txt || (echo "llm.txt not found" && exit 1)
	@test -f llm-full.txt || (echo "llm-full.txt not found" && exit 1)
	@echo "Documentation files generated successfully"

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
