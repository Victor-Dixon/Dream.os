#!/usr/bin/env python3
"""
Sandbox Manager Module - Synthetic GitHub
=========================================

<!-- SSOT Domain: integration -->

Extracted from synthetic_github.py for V2 compliance.
Handles GitHub sandbox mode (offline/local-only mode) management.

V2 Compliance | Author: Agent-1 | Date: 2025-12-13
"""

from __future__ import annotations

import json
import logging
import subprocess
from pathlib import Path
from typing import Dict, Any, Optional

from ..config.timeout_constants import TimeoutConstants

logger = logging.getLogger(__name__)


class GitHubSandboxMode:
    """Manages GitHub sandbox mode (offline/local-only mode)."""
    
    def __init__(self, config_file: Optional[Path] = None):
        """
        Initialize sandbox mode manager.
        
        Args:
            config_file: Path to sandbox config file
        """
        if config_file is None:
            project_root = Path(__file__).resolve().parent.parent.parent
            config_file = project_root / "github_sandbox_mode.json"
        
        self.config_file = Path(config_file)
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load sandbox mode configuration."""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                logger.warning(f"Failed to load sandbox config: {e}")
        
        return {
            "sandbox_mode": False,
            "reason": None,
            "enabled_at": None,
            "auto_detect": True
        }
    
    def _save_config(self):
        """Save sandbox mode configuration."""
        try:
            self.config_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save sandbox config: {e}")
    
    def is_enabled(self) -> bool:
        """Check if sandbox mode is enabled."""
        if self.config.get("sandbox_mode"):
            return True
        
        # Auto-detect if enabled
        if self.config.get("auto_detect", True):
            return not self._detect_github_availability()
        
        return False
    
    def _detect_github_availability(self) -> bool:
        """Detect if GitHub is available."""
        try:
            # Quick check - try to ping GitHub
            result = subprocess.run(
                ["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", 
                 "https://api.github.com/zen"],
                capture_output=True,
                text=True,
                timeout=TimeoutConstants.HTTP_QUICK
            )
            
            # Fallback: try python requests if curl not available
            if result.returncode != 0:
                try:
                    import requests
                    response = requests.get(
                        "https://api.github.com/zen", 
                        timeout=TimeoutConstants.HTTP_QUICK
                    )
                    return response.status_code == 200
                except Exception:
                    return False
            
            return result.stdout.strip() == "200"
            
        except Exception as e:
            logger.debug(f"GitHub availability check failed: {e}")
            return False
    
    def enable(self, reason: str = "manual"):
        """Enable sandbox mode."""
        self.config["sandbox_mode"] = True
        self.config["reason"] = reason
        self.config["enabled_at"] = str(Path(__file__).stat().st_mtime)
        self._save_config()
        logger.info(f"🔒 Sandbox mode enabled: {reason}")
    
    def disable(self):
        """Disable sandbox mode."""
        self.config["sandbox_mode"] = False
        self.config["reason"] = None
        self.config["enabled_at"] = None
        self._save_config()
        logger.info("✅ Sandbox mode disabled")



