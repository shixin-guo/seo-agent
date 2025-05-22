"""Setup configuration for the seo-agent package.

This module contains the package configuration
and dependencies for the seo-agent project,
an AI-powered SEO automation tool. It uses setuptools to manage package installation,
dependencies, and entry points.
"""

from setuptools import find_packages, setup

with open("README.md", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="seo-agent",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="AI-powered SEO automation tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/seo-agent",
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.11",
    install_requires=[
        "dspy-ai>=2.0.0",
        "python-dotenv>=1.0.0",
        "pyyaml>=6.0",
        "click>=8.1.0",
        "tqdm>=4.66.0",
        "requests>=2.30.0",
        "beautifulsoup4>=4.12.0",
        "pandas>=2.0.0",
    ],
    extras_require={
        "dev": [
            "ruff>=0.1.6",
            "mypy>=1.3.0",
            "pre-commit>=3.3.2",
            "types-requests>=2.31.0",
            "types-PyYAML>=6.0.12",
        ],
    },
    entry_points={
        "console_scripts": [
            "seo-agent=main:cli",
        ],
    },
)
