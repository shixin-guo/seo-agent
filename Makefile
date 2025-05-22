.PHONY: init lint format typecheck test mock clean

init:
	pip install -r requirements-dev.txt
	pre-commit install

lint:
	ruff check seo_agent main.py --extend-exclude tests/

format:
	ruff format seo_agent main.py
	ruff check --fix seo_agent main.py

typecheck:
	mypy seo_agent main.py

test:
	pytest

test-unit:
	pytest -m unit

test-integration:
	pytest -m integration

test-cov:
	pytest --cov=seo_agent --cov-report=term --cov-report=xml --cov-report=html

# Run the mock demo without API keys
mock:
	python tests/mock/simple_keyword_demo.py --seed "digital marketing" --industry "saas" --auto-csv

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
