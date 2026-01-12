# Agent Cellphone V2 Documentation

This directory contains the Sphinx-based API documentation for Agent Cellphone V2.

## Building Documentation

### Prerequisites
pip install -r requirements.txt

### Quick Build
make html

### Advanced Build
make clean-all && make autodoc && make html && make serve

## Documentation Structure

- conf.py: Sphinx configuration
- index.rst: Main documentation page  
- _static/: Static assets (CSS, images)
- api/: Auto-generated API docs
- examples/: Usage examples

## Custom Styling

Uses swarm-themed design with gold, orange, and purple colors.

🐝 WE. ARE. SWARM. ⚡️🔥
