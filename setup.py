#!/usr/bin/env python
"""
Setup script for Agent Cellphone V2 - Swarm AI Coordination Framework
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README
this_directory = Path(__file__).parent
long_description = (this_directory / "PYPI_PACKAGE_README.md").read_text()

# Read version from package
def get_version():
    """Extract version from __init__.py"""
    init_file = this_directory / "src" / "__init__.py"
    if init_file.exists():
        content = init_file.read_text()
        for line in content.split('\n'):
            if line.startswith('__version__'):
                return line.split('=')[1].strip().strip('"\'')

    # Fallback version
    return "2.0.0"

setup(
    name="agent-cellphone-v2",
    version=get_version(),
    author="Agent Cellphone Development Team",
    author_email="team@agent-cellphone-v2.com",
    description="Swarm AI Coordination Framework for Multi-Agent Collaboration",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/your-org/agent-cellphone-v2",
    project_urls={
        "Documentation": "https://docs.agent-cellphone-v2.com",
        "Source": "https://github.com/your-org/agent-cellphone-v2",
        "Tracker": "https://github.com/your-org/agent-cellphone-v2/issues",
        "Changelog": "https://github.com/your-org/agent-cellphone-v2/blob/main/CHANGELOG.md",
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Distributed Computing",
    ],
    keywords=[
        "ai", "swarm", "agents", "coordination", "collaboration",
        "multi-agent", "artificial-intelligence", "distributed-systems",
        "machine-learning", "automation"
    ],
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.8",
    install_requires=[
        # Core dependencies (none required for basic functionality)
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=22.0.0",
            "flake8>=5.0.0",
            "mypy>=1.0.0",
            "sphinx>=5.0.0",
            "sphinx-rtd-theme>=1.2.0",
            "pre-commit>=3.0.0",
        ],
        "monitoring": [
            "prometheus-client>=0.16.0",
            "grafana-api>=1.0.3",
        ],
        "security": [
            "cryptography>=41.0.0",
            "pyjwt>=2.0.0",
        ],
        "web": [
            "fastapi>=0.100.0",
            "uvicorn>=0.23.0",
            "websockets>=11.0.0",
        ],
        "all": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=22.0.0",
            "flake8>=5.0.0",
            "mypy>=1.0.0",
            "sphinx>=5.0.0",
            "sphinx-rtd-theme>=1.2.0",
            "pre-commit>=3.0.0",
            "prometheus-client>=0.16.0",
            "grafana-api>=1.0.3",
            "cryptography>=41.0.0",
            "pyjwt>=2.0.0",
            "fastapi>=0.100.0",
            "uvicorn>=0.23.0",
            "websockets>=11.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "agent-cellphone=agent_cellphone.cli:main",
            "agent-cellphone-monitor=agent_cellphone.cli:monitor",
            "agent-cellphone-status=agent_cellphone.cli:status",
            "agent-cellphone-coordinate=agent_cellphone.cli:coordinate",
            "agent-cellphone-dashboard=agent_cellphone.cli:dashboard",
            "agent-cellphone-metrics=agent_cellphone.cli:metrics",
            "agent-cellphone-health=agent_cellphone.cli:health",
        ],
    },
    include_package_data=True,
    zip_safe=False,
    test_suite="tests",
    tests_require=[
        "pytest>=7.0.0",
        "pytest-cov>=4.0.0",
    ],
)</content>
</xai:function_call<parameter name="path">D:\Agent_Cellphone_V2_Repository\setup.py