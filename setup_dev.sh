#!/bin/bash

# Setup development environment for SEO Agent

echo "Setting up development environment..."

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Initialize pre-commit hooks
echo "Setting up pre-commit hooks..."
pre-commit install

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "Creating .env file from template..."
    cp .env.template .env
    echo "Please edit .env file with your API keys"
fi

echo "Setup complete! Activate the virtual environment with:"
echo "source venv/bin/activate"
