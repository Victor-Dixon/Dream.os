.. Agent Cellphone V2 documentation master file, created by
   sphinx-quickstart on Tue Jan 11 22:50:00 2026.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Agent Cellphone V2 - Swarm Intelligence Platform
================================================

.. image:: _static/logo.png
   :alt: Agent Cellphone V2 Logo
   :align: center

**A multi-agent swarm intelligence system for coordinated task execution and collective decision making.**

🐝 **WE. ARE. SWARM.** ⚡️🔥

Overview
--------

Agent Cellphone V2 is a revolutionary multi-agent system that enables swarm intelligence
through coordinated task execution, consensus-driven decision making, and automated
agent coordination. Built with V2 compliance standards and SOLID architectural principles.

Key Features
~~~~~~~~~~~~

- **🤖 Multi-Agent Coordination**: Seamless communication between 8+ specialized agents
- **📨 Unified Messaging System**: Single source of truth for all inter-agent communication
- **🎯 Swarm Intelligence**: Collective decision making through consensus algorithms
- **🔧 PyAutoGUI Integration**: Programmatic UI control for agent interaction
- **📊 Discord Integration**: Real-time monitoring and control through Discord bot
- **🛡️ V2 Compliance**: Enterprise-grade architecture with comprehensive testing

Quick Start
-----------

.. code-block:: bash

   # Clone and setup
   git clone https://github.com/your-org/agent-cellphone-v2.git
   cd agent-cellphone-v2

   # Configure environment
   cp env.example .env
   # Edit .env with Discord credentials

   # Install dependencies
   pip install -r requirements.txt

   # Run examples
   python examples/two_agent_setup.py

Table of Contents
-----------------

.. toctree::
   :maxdepth: 2
   :caption: Getting Started:

   installation
   quickstart
   examples/index

.. toctree::
   :maxdepth: 2
   :caption: Core Systems:

   core/messaging
   core/agents
   core/coordination
   core/consensus

.. toctree::
   :maxdepth: 2
   :caption: Services:

   services/messaging_cli
   services/onboarding
   services/discord

.. toctree::
   :maxdepth: 2
   :caption: API Reference:

   api/core
   api/services
   api/discord

.. toctree::
   :maxdepth: 2
   :caption: Development:

   contributing
   development/setup
   development/testing
   development/deployment

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

Architecture Overview
=====================

.. image:: _static/architecture_diagram.png
   :alt: System Architecture
   :align: center

The system follows a modular, V2-compliant architecture with clear separation of concerns:

- **Core Layer**: Fundamental messaging, coordination, and consensus systems
- **Service Layer**: Business logic and external integrations
- **Agent Layer**: Specialized agent implementations
- **Interface Layer**: CLI, Discord bot, and API interfaces

V2 Compliance
=============

Agent Cellphone V2 maintains strict adherence to V2 architectural standards:

✅ **SOLID Principles**: Single Responsibility, Open/Closed, Liskov Substitution, Interface Segregation, Dependency Inversion

✅ **Modular Architecture**: Modules <300 lines, <5 classes, <10 functions

✅ **SSOT (Single Source of Truth)**: No code duplication, centralized configuration

✅ **Comprehensive Testing**: Unit, integration, and end-to-end test coverage

✅ **Documentation**: Complete API documentation with examples

Support
=======

- **Documentation**: https://agent-cellphone-v2.readthedocs.io/
- **GitHub Issues**: Bug reports and feature requests
- **Discord**: Real-time community support
- **Contributing Guide**: See :doc:`contributing`

License
=======

Agent Cellphone V2 is licensed under the MIT License. See LICENSE file for details.

.. note::
   This documentation is automatically generated from docstrings and RST files.
   Last updated: |today|