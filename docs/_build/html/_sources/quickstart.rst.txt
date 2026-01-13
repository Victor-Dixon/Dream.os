Quick Start Guide
=================

Get up and running with Agent Cellphone V2 in minutes!

🚀 **3-Step Quick Start**

Step 1: Basic Setup (5 minutes)
--------------------------------

1. **Install and Configure** (see :doc:`installation`)

2. **Create Agent Workspace**

   .. code-block:: bash

      # Create workspace for Agent-1
      mkdir -p agent_workspaces/Agent-1/inbox
      mkdir -p agent_workspaces/Agent-1/archive

3. **Start Basic Agent**

   .. code-block:: bash

      # Start messaging queue processor
      python -m src.services.messaging_cli --start-queue

      # In another terminal, start the Discord bot
      python -m src.discord_commander.bot_runner_v2

Step 2: Send First Message (2 minutes)
---------------------------------------

.. code-block:: bash

   # Send a test message
   python -m src.services.messaging_cli \
     --agent Agent-1 \
     --message "Hello Agent-1! This is your first message." \
     --sender "CAPTAIN"

   # Check agent inbox
   ls agent_workspaces/Agent-1/inbox/

Step 3: Try Examples (3 minutes)
---------------------------------

Run the included examples:

.. code-block:: bash

   # Two-agent coordination example
   python examples/two_agent_setup.py

   # Full swarm demonstration
   python examples/full_swarm.py

   # Consensus decision making
   python examples/consensus_demo.py

🎯 **What Just Happened?**

You successfully:

- ✅ **Configured** a multi-agent swarm system
- ✅ **Started** messaging and Discord services
- ✅ **Sent** your first inter-agent message
- ✅ **Ran** example coordination scenarios
- ✅ **Experienced** swarm intelligence in action

🔧 **Next Steps**

1. **Explore Features**:
   - Try different message types and priorities
   - Experiment with agent-to-agent communication
   - Test consensus algorithms

2. **Customize Agents**:
   - Create specialized agent roles
   - Add custom commands and behaviors
   - Integrate external APIs

3. **Scale Up**:
   - Add more agents (up to 8 supported)
   - Configure advanced coordination patterns
   - Set up monitoring and analytics

📚 **Learn More**

- :doc:`examples/index` - Complete example walkthroughs
- :doc:`core/messaging` - Deep dive into messaging system
- :doc:`api/core` - Full API reference
- :doc:`contributing` - Join development

🐝 **Welcome to the Swarm!**

You've successfully activated your first multi-agent swarm intelligence system.
The agents are now ready to coordinate, collaborate, and execute tasks collectively.

**Happy swarming!** ⚡️🔥🤖