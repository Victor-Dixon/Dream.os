#!/usr/bin/env python3
"""
Cleanup Execution - Phase 1: Configuration Consolidation
=======================================================

Execute Phase 1 of the root directory cleanup plan.
Moves configuration files and consolidates them.

Author: Agent-1 (Integration & Core Systems Specialist)
Phase 1 Lead - Infrastructure Consolidation
Created: 2026-01-13
"""

import json
import shutil
from pathlib import Path
from typing import Dict, List, Any

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CleanupExecutor:
    """Executes the cleanup plan phase by phase."""

    def __init__(self, base_path: str = "D:\\Agent_Cellphone_V2_Repository"):
        self.base_path = Path(base_path)
        self.phase1_results = {
            "phase": "configuration_consolidation",
            "timestamp": "2026-01-13T05:40:00",
            "actions_completed": [],
            "issues": [],
            "success": True
        }

    def execute_phase1(self) -> Dict[str, Any]:
        """Execute Phase 1: Configuration consolidation."""
        logger.info("🚀 Starting Phase 1: Configuration Consolidation...")

        try:
            # 1.1 Environment Variables (4 → 1)
            self._consolidate_env_files()

            # 1.2 Agent & Coordination Configs (7 → 2)
            self._consolidate_agent_configs()
            self._consolidate_coordination_configs()

            # 1.3 Test & Build Configs (4 → 1)
            self._consolidate_test_configs()

            # 1.4 Result Archives (4 → 0)
            self._archive_result_files()

            logger.info("✅ Phase 1 Configuration Consolidation completed successfully!")

        except Exception as e:
            logger.error(f"❌ Phase 1 failed: {e}")
            self.phase1_results["success"] = False
            self.phase1_results["issues"].append(str(e))

        return self.phase1_results

    def _consolidate_env_files(self):
        """Move environment files to archives, keep .env.example."""
        logger.info("📁 Consolidating environment files...")

        env_files = [".env", ".env.backup", ".env.discord"]
        archive_dir = self.base_path / "config" / "archives"

        for env_file in env_files:
            src = self.base_path / env_file
            if src.exists():
                dst = archive_dir / f"{env_file}.archived"
                shutil.move(str(src), str(dst))
                logger.info(f"  Moved {env_file} → config/archives/")
                self.phase1_results["actions_completed"].append(f"Archived {env_file}")

        # Ensure .env.example exists in root
        env_example = self.base_path / ".env.example"
        if not env_example.exists():
            # Create a template if it doesn't exist
            template_content = """# Environment Variables Template
# Copy this file to .env and fill in your values

# Discord Bot Configuration
DISCORD_BOT_TOKEN=your_bot_token_here
DISCORD_CHANNEL_ID=your_channel_id_here

# API Keys
OPENAI_API_KEY=your_openai_key_here

# Database Configuration
DATABASE_URL=sqlite:///data/unified.db

# Other Configuration
LOG_LEVEL=INFO
"""
            env_example.write_text(template_content)
            logger.info("  Created .env.example template")
            self.phase1_results["actions_completed"].append("Created .env.example template")

    def _consolidate_agent_configs(self):
        """Merge agent_mode_config.json and cursor_agent_coords.json."""
        logger.info("🔧 Consolidating agent configuration files...")

        config_dir = self.base_path / "config"
        agent_config_file = config_dir / "agent_config.json"

        # Read existing configs
        agent_mode_config = {}
        cursor_coords_config = {}

        # Read agent_mode_config.json
        agent_mode_file = self.base_path / "agent_mode_config.json"
        if agent_mode_file.exists():
            try:
                with open(agent_mode_file, 'r', encoding='utf-8') as f:
                    agent_mode_config = json.load(f)
            except Exception as e:
                logger.warning(f"Failed to read agent_mode_config.json: {e}")

        # Read cursor_agent_coords.json
        cursor_coords_file = self.base_path / "cursor_agent_coords.json"
        if cursor_coords_file.exists():
            try:
                with open(cursor_coords_file, 'r', encoding='utf-8') as f:
                    cursor_coords_config = json.load(f)
            except Exception as e:
                logger.warning(f"Failed to read cursor_agent_coords.json: {e}")

        # Merge configurations
        merged_config = {
            "metadata": {
                "created": "2026-01-13T05:40:00",
                "source": "merged_from_agent_mode_config_and_cursor_coords",
                "purpose": "consolidated_agent_configuration"
            },
            "agent_modes": agent_mode_config,
            "coordinates": cursor_coords_config
        }

        # Write merged config
        with open(agent_config_file, 'w', encoding='utf-8') as f:
            json.dump(merged_config, f, indent=2, ensure_ascii=False)

        # Archive original files
        archive_dir = config_dir / "archives"
        for orig_file in [agent_mode_file, cursor_coords_file]:
            if orig_file.exists():
                dst = archive_dir / f"{orig_file.name}.archived"
                shutil.move(str(orig_file), str(dst))
                logger.info(f"  Archived {orig_file.name} → config/archives/")

        logger.info("  Created config/agent_config.json with merged configurations")
        self.phase1_results["actions_completed"].append("Merged agent configurations into config/agent_config.json")

    def _consolidate_coordination_configs(self):
        """Merge coordination_cache.json and swarm_synchronization_20260113.json."""
        logger.info("🔗 Consolidating coordination configuration files...")

        config_dir = self.base_path / "config"
        coord_config_file = config_dir / "coordination_config.json"

        # Read existing configs
        coord_cache_config = {}
        swarm_sync_config = {}

        # Read coordination_cache.json
        coord_cache_file = self.base_path / "coordination_cache.json"
        if coord_cache_file.exists():
            try:
                with open(coord_cache_file, 'r', encoding='utf-8') as f:
                    coord_cache_config = json.load(f)
            except Exception as e:
                logger.warning(f"Failed to read coordination_cache.json: {e}")

        # Read swarm_synchronization_20260113.json
        swarm_sync_file = self.base_path / "swarm_synchronization_20260113.json"
        if swarm_sync_file.exists():
            try:
                with open(swarm_sync_file, 'r', encoding='utf-8') as f:
                    swarm_sync_config = json.load(f)
            except Exception as e:
                logger.warning(f"Failed to read swarm_synchronization_20260113.json: {e}")

        # Merge configurations
        merged_config = {
            "metadata": {
                "created": "2026-01-13T05:40:00",
                "source": "merged_from_coordination_cache_and_swarm_sync",
                "purpose": "consolidated_coordination_configuration"
            },
            "coordination_cache": coord_cache_config,
            "swarm_synchronization": swarm_sync_config
        }

        # Write merged config
        with open(coord_config_file, 'w', encoding='utf-8') as f:
            json.dump(merged_config, f, indent=2, ensure_ascii=False)

        # Archive original files
        archive_dir = config_dir / "archives"
        for orig_file in [coord_cache_file, swarm_sync_file]:
            if orig_file.exists():
                dst = archive_dir / f"{orig_file.name}.archived"
                shutil.move(str(orig_file), str(dst))
                logger.info(f"  Archived {orig_file.name} → config/archives/")

        logger.info("  Created config/coordination_config.json with merged configurations")
        self.phase1_results["actions_completed"].append("Merged coordination configurations into config/coordination_config.json")

    def _consolidate_test_configs(self):
        """Consolidate pytest.ini and audit_plan.yaml into testing_config.toml."""
        logger.info("🧪 Consolidating test configuration files...")

        config_dir = self.base_path / "config"
        test_config_file = config_dir / "testing_config.toml"

        # Read existing configs
        pytest_config = ""
        audit_plan_config = {}

        # Read pytest.ini
        pytest_file = self.base_path / "pytest.ini"
        if pytest_file.exists():
            try:
                pytest_config = pytest_file.read_text(encoding='utf-8')
            except Exception as e:
                logger.warning(f"Failed to read pytest.ini: {e}")

        # Read audit_plan.yaml
        audit_plan_file = self.base_path / "audit_plan.yaml"
        if audit_plan_file.exists():
            try:
                import yaml
                with open(audit_plan_file, 'r', encoding='utf-8') as f:
                    audit_plan_config = yaml.safe_load(f) or {}
            except Exception as e:
                logger.warning(f"Failed to read audit_plan.yaml: {e}")

        # Create consolidated TOML config
        toml_content = f"""# Consolidated Testing Configuration
# Created: 2026-01-13
# Source: pytest.ini + audit_plan.yaml

[tool.pytest.ini_options]
{pytest_config}

[audit_plan]
# Converted from audit_plan.yaml
plan_data = {json.dumps(audit_plan_config, indent=2)}
"""

        # Write consolidated config
        with open(test_config_file, 'w', encoding='utf-8') as f:
            f.write(toml_content)

        # Archive original files
        archive_dir = config_dir / "archives"
        for orig_file in [pytest_file, audit_plan_file]:
            if orig_file.exists():
                dst = archive_dir / f"{orig_file.name}.archived"
                shutil.move(str(orig_file), str(dst))
                logger.info(f"  Archived {orig_file.name} → config/archives/")

        logger.info("  Created config/testing_config.toml with consolidated test configs")
        self.phase1_results["actions_completed"].append("Consolidated test configurations into config/testing_config.toml")

    def _archive_result_files(self):
        """Move result JSON files to reports/archives/."""
        logger.info("📊 Archiving result files...")

        result_files = [
            "database_audit_results.json",
            "database_qa_integration_results.json",
            "database_validation_results.json",
            "integration_test_results.json"
        ]

        reports_archive_dir = self.base_path / "reports" / "archives"

        for result_file in result_files:
            src = self.base_path / result_file
            if src.exists():
                dst = reports_archive_dir / result_file
                shutil.move(str(src), str(dst))
                logger.info(f"  Moved {result_file} → reports/archives/")
                self.phase1_results["actions_completed"].append(f"Archived {result_file} to reports/archives")


def main():
    """Execute Phase 1 cleanup."""
    print("🚀 Phase 1: Configuration Consolidation")
    print("=" * 50)

    executor = CleanupExecutor()
    results = executor.execute_phase1()

    # Print results
    print("\n📊 PHASE 1 RESULTS:")
    print(f"Success: {'✅' if results['success'] else '❌'}")
    print(f"Actions completed: {len(results['actions_completed'])}")

    if results["actions_completed"]:
        print("\n✅ COMPLETED ACTIONS:")
        for action in results["actions_completed"]:
            print(f"  • {action}")

    if results["issues"]:
        print("\n🚨 ISSUES:")
        for issue in results["issues"]:
            print(f"  • {issue}")

    # Save results
    output_file = "phase1_cleanup_results.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print(f"\n📄 Results saved to: {output_file}")

    if results["success"]:
        print("\n🎉 Phase 1 Configuration Consolidation: SUCCESS!")
        print("Ready to proceed to Phase 2: Documentation Relocation")
    else:
        print("\n⚠️ Phase 1 had issues. Review and resolve before proceeding.")


if __name__ == "__main__":
    main()