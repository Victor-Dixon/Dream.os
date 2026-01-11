#!/usr/bin/env python3
"""
Agent Cellphone V2 - Python Package Setup
=========================================

Standard setuptools-based package installation.

Usage:
    pip install -e .           # Development install
    pip install .              # Production install
    python setup.py develop    # Alternative dev install
"""

from setuptools import setup, find_packages
import os
from pathlib import Path

# Read version from version file
def read_version():
    version_file = Path(__file__).parent / "src" / "agent_cellphone_v2" / "__version__.py"
    if version_file.exists():
        exec(version_file.read_text())
        return locals()["__version__"]
    return "2.0.0"

# Read README
def read_readme():
    readme_file = Path(__file__).parent / "README.md"
    if readme_file.exists():
        return readme_file.read_text()
    return "Agent Cellphone V2 - Multi-Agent Coordination System"

setup(
    name="agent-cellphone-v2",
    version=read_version(),
    description="Agent Cellphone V2 - Multi-Agent Coordination System",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    author="DadudeCK",
    author_email="dadudekc@gmail.com",
    url="https://github.com/dadudekc/agent-cellphone-v2",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    python_requires=">=3.11",
    install_requires=[
        # Runtime dependencies
        "python-dotenv>=1.0.0",
        "pyyaml>=6.0.0",
        "pydantic>=2.0.0",
        "pydantic-settings>=2.0.0",
        "requests>=2.31.0",
        "aiohttp>=3.8.0",
        "fastapi>=0.100.0",
        "uvicorn[standard]>=0.23.0",
        "discord.py>=2.3.0",
        "pyautogui>=0.9.54",
        "pyperclip>=1.8.0",
    ],
    extras_require={
        "dev": [
            "black>=23.0.0",
            "flake8>=6.0.0",
            "isort>=5.12.0",
            "mypy>=1.0.0",
            "pre-commit>=3.0.0",
            "pylint>=2.17.0",
        ],
        "test": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "pytest-asyncio>=0.21.0",
            "pytest-xdist>=3.0.0",
            "pytest-timeout>=2.0.0",
        ],
        "docs": [
            "sphinx>=5.0.0",
            "sphinx-rtd-theme>=1.2.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "agent-cellphone=main:main",
            "ac2-messaging=src.services.messaging_cli:main",
            "ac2-status=src.services.status_cli:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Distributed Computing",
    ],
    keywords="agents automation swarm coordination ai",
    project_urls={
        "Bug Reports": "https://github.com/dadudekc/agent-cellphone-v2/issues",
        "Source": "https://github.com/dadudekc/agent-cellphone-v2",
        "Documentation": "https://agent-cellphone-v2.readthedocs.io/",
    },
)