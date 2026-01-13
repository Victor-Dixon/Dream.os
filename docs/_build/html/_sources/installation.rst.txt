Installation Guide
==================

This guide will help you install and set up Agent Cellphone V2 on your system.

System Requirements
-------------------

- **Python**: 3.11 or higher
- **Operating System**: Windows 10/11, macOS 10.15+, Ubuntu 18.04+
- **Memory**: Minimum 4GB RAM, 8GB recommended
- **Storage**: 2GB free space
- **Network**: Internet connection for Discord integration

Prerequisites
-------------

1. **Python Installation**

   Download and install Python 3.11+ from the official website:

   - `https://python.org/downloads/`

   Verify installation:

   .. code-block:: bash

      python --version
      # Should show Python 3.11.x or higher

2. **Git Installation**

   Download and install Git from:

   - `https://git-scm.com/downloads`

   Verify installation:

   .. code-block:: bash

      git --version

3. **Discord Bot Token**

   Create a Discord application at:

   - `https://discord.com/developers/applications`

   Copy the bot token for configuration.

Installation Steps
------------------

1. **Clone the Repository**

   .. code-block:: bash

      git clone https://github.com/your-org/agent-cellphone-v2.git
      cd agent-cellphone-v2

2. **Create Virtual Environment** (Recommended)

   .. code-block:: bash

      python -m venv venv

      # Activate virtual environment
      # Windows:
      venv\\Scripts\\activate
      # macOS/Linux:
      source venv/bin/activate

3. **Install Dependencies**

   .. code-block:: bash

      pip install -r requirements.txt
      pip install -r requirements-dev.txt

4. **Configure Environment**

   Copy the example environment file:

   .. code-block:: bash

      cp env.example .env

   Edit `.env` file with your configuration:

   .. code-block:: ini

      # Discord Bot Configuration (Required)
      DISCORD_BOT_TOKEN=your_discord_bot_token_here
      DISCORD_GUILD_ID=your_discord_server_id_here

      # Optional: API Keys for extended functionality
      OPENAI_API_KEY=your_openai_key_here
      ANTHROPIC_API_KEY=your_anthropic_key_here

5. **Verify Installation**

   Run a basic test:

   .. code-block:: bash

      python -c "import src.core.messaging_core; print('✅ Installation successful')"

Troubleshooting
---------------

**Common Issues:**

1. **Permission Error on Windows**

   Run command prompt as Administrator or use:

   .. code-block:: powershell

      Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

2. **Module Import Errors**

   Ensure you're in the virtual environment:

   .. code-block:: bash

      # Check active environment
      which python
      # Should point to venv/bin/python or venv\\Scripts\\python.exe

3. **Discord Connection Issues**

   - Verify bot token is correct
   - Ensure bot has proper permissions in Discord server
   - Check network connectivity

Next Steps
----------

After successful installation:

1. **Run Examples**: Try `python examples/two_agent_setup.py`
2. **Read Documentation**: Visit `docs/_build/html/index.html`
3. **Join Development**: See :doc:`contributing`