import os
import json
import logging
import datetime
from typing import List, Dict, Optional, Any
from Agents.core.AgentBase import AgentBase  

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class JournalAgent(AgentBase):
    """
    AI-powered agent for managing dev logs & blog entries.
    
    ✅ Auto-generates structured dev logs from debugging sessions.
    ✅ Summarizes issues, fixes, and key improvements for documentation.
    ✅ Exports Markdown-formatted dev blogs for easy publishing.
    """

    JOURNAL_DIR = "dev_logs"

    def __init__(self):
        """
        Initializes the JournalAgent, ensuring the storage path exists.
        """
        super().__init__(name="JournalAgent", project_name="AI_Debugger_Assistant")
        os.makedirs(self.JOURNAL_DIR, exist_ok=True)
        logger.info(f"📁 JournalAgent initialized. Storage path: {self.JOURNAL_DIR}")

    def _get_log_filepath(self, title: str) -> str:
        """Creates a safe filename for the log entry."""
        safe_title = "".join(c for c in title if c.isalnum() or c in (" ", "_")).rstrip()
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        return os.path.join(self.JOURNAL_DIR, f"{safe_title}_{timestamp}.json")

    def create_dev_log(self, issue: str, resolution: str, category: str, status: str = "✅ Fixed") -> Dict[str, Any]:
        """
        Creates and saves a structured dev log entry.

        Args:
            issue (str): Description of the problem.
            resolution (str): How the problem was fixed or optimized.
            category (str): Type of update (Bug Fix, Feature, Optimization, AI Tuning).
            status (str): Fix status (✅ Fixed, 🔄 Work in Progress, ❌ Not Resolved).

        Returns:
            Dict[str, Any]: File path and entry metadata.
        """
        filepath = self._get_log_filepath(issue)
        timestamp = datetime.datetime.now().isoformat()

        entry = {
            "timestamp": timestamp,
            "issue": issue,
            "resolution": resolution,
            "category": category,
            "status": status
        }

        try:
            with open(filepath, "w", encoding="utf-8") as file:
                json.dump(entry, file, indent=4)
            logger.info(f"✅ Dev log created: {filepath}")
            return {"status": "success", "file_path": filepath}
        except IOError as e:
            logger.error(f"❌ Error creating dev log: {e}")
            return {"status": "error", "message": str(e)}

    def generate_markdown_report(self, entries: List[Dict[str, Any]]) -> str:
        """
        Generates a Markdown-formatted dev update report.

        Args:
            entries (List[Dict[str, Any]]): List of dev log entries.

        Returns:
            str: Markdown-formatted report.
        """
        report = "# Dev Update – {}\n\n".format(datetime.datetime.now().strftime("%B %Y"))

        for entry in entries:
            report += f"## 🛠️ [{entry['category']}] {entry['issue']}\n"
            report += f"**Issue:** {entry['issue']}\n"
            report += f"**Solution:** {entry['resolution']}\n"
            report += f"**Status:** {entry['status']}\n\n"

        return report

    def list_dev_logs(self) -> List[Dict[str, Any]]:
        """
        Lists all dev logs in the journal directory.

        Returns:
            List[Dict[str, Any]]: List of journal metadata.
        """
        entries = []
        for filename in os.listdir(self.JOURNAL_DIR):
            if filename.endswith(".json"):
                with open(os.path.join(self.JOURNAL_DIR, filename), "r", encoding="utf-8") as file:
                    entry_data = json.load(file)
                    entries.append(entry_data)

        logger.info(f"📜 Listed {len(entries)} dev logs.")
        return entries

    def generate_full_dev_blog(self) -> str:
        """
        Generates a full dev blog post by compiling all saved logs.

        Returns:
            str: Complete Markdown blog content.
        """
        logs = self.list_dev_logs()
        return self.generate_markdown_report(logs)

    def solve_task(self, task: str, **kwargs) -> Dict[str, Any]:
        """
        Dispatches journal-related tasks dynamically.

        Args:
            task (str): The operation to perform.
            **kwargs: Additional arguments for the task.

        Returns:
            Dict[str, Any]: The result of the operation.
        """
        task_methods = {
            "create": self.create_dev_log,
            "list": self.list_dev_logs,
            "generate_blog": self.generate_full_dev_blog,
        }

        if task in task_methods:
            return task_methods[task](**kwargs)
        else:
            logger.error(f"❌ Invalid task '{task}'")
            return {"status": "error", "message": f"Invalid task '{task}'"}
