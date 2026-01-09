# Memory system configuration
from pathlib import Path

# Database paths
MEMORY_DB_PATH = Path(__file__).parent.parent / "data" / "dreamos_memory.db"
RESUME_DB_PATH = Path(__file__).parent.parent.parent / "gamification" / "data" / "dreamos_resume.db"
TOOLS_DB_PATH = Path(__file__).parent.parent.parent.parent / "tools" / "code_analysis" / "data" / "tools.db"
TEMPLATES_DB_PATH = Path(__file__).parent.parent.parent / "templates" / "data" / "templates.db"
