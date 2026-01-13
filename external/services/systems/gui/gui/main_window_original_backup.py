#!/usr/bin/env python3
"""
Thea Main Window - Dreamscape MMORPG Platform GUI
"""

import sys
from dreamscape.gui.debug_handler import debug_button
import os
import logging
from pathlib import Path
from typing import Any

from dreamscape.gui.controllers import MainController
from dreamscape.core.config import MEMORY_DB_PATH, RESUME_DB_PATH

# Restore UTF-8 console encoding on Windows prior to configuring logging
if sys.platform.startswith("win") and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        # Fallback for older consoles
        try:
            os.system("chcp 65001 > nul")
        except Exception:
            pass

# EDIT START: ensure root logger streams text as UTF-8 (avoids UnicodeEncodeError on Windows)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
    encoding="utf-8",
    force=True,
)
# EDIT END

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QStackedWidget,
    QFrame,
    QStatusBar,
    QMessageBox,
    QProgressDialog,
    QTabWidget,
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QFont

# Import core systems
from dreamscape.core.memory import MemoryManager
from dreamscape.core.mmorpg.mmorpg_engine import MMORPGEngine
from dreamscape.core.legacy.resume_tracker import ResumeTracker
from dreamscape.core.mmorpg.enhanced_skill_resume_system import (
    EnhancedSkillResumeSystem,
)
from dreamscape.core.discord import DiscordManager
from dreamscape.core.scraping_system import ScraperOrchestrator
from dreamscape.core.dreamscape_processor import DreamscapeProcessor
from dreamscape.core.templates.prompt_deployer import PromptDeployer
from dreamscape.core.settings_manager import settings_manager

# from dreamscape.core.workflow_system import initialize_live_processor, get_live_processor  # TODO: Use workflow_system after consolidation

# Import modular panels
from .panels.dashboard_panel import DashboardPanel
from .panels.conversations_panel import ConversationsPanel
from dreamscape.gui.panels.analytics_panel import AnalyticsPanel
from dreamscape.gui.panels.content_analytics_panel import ContentAnalyticsPanel
from dreamscape.gui.panels.enhanced_analytics_panel import EnhancedAnalyticsPanel
from dreamscape.gui.panels.resume_panel import ResumePanel
from dreamscape.gui.panels.scraper_panel import ScraperPanel
from dreamscape.gui.panels.task_panel import TaskPanel
from dreamscape.gui.panels.quest_log_panel import QuestLogPanel
from dreamscape.gui.panels.export_panel import ExportPanel
from dreamscape.gui.panels.enhanced_devlog_panel import EnhancedDevlogPanel
from dreamscape.gui.panels.skill_tree_panel import SkillTreePanel
from dreamscape.gui.panels.workflow_panel import WorkflowPanel
from dreamscape.gui.panels.gamification_panel import GamificationPanel
from dreamscape.gui.panels.voice_modeling_panel import VoiceModelingPanel
from dreamscape.gui.panels.community_templates_panel import CommunityTemplatesPanel
from dreamscape.gui.panels.templates_panel import TemplatesPanel
from dreamscape.gui.panels.settings_panel import SettingsPanel
# EDIT START: Import CombatEnginePanel for Advanced Features integration
from dreamscape.gui.panels.combat_engine_panel import CombatEnginePanel
# EDIT END

# Import Unified Export Center
from .components.unified_export_center import UnifiedExportCenter

# Import loading screen
from .components.loading_screen import LoadingManager
from .components.ftue_welcome_modal import (
    FTUEWelcomeModal,
)  # EDIT: FTUE onboarding modal import

# EDIT START: Consolidation import update
from dreamscape.core.legacy.conversation_system import (
    ConversationStatsUpdater,
)  # Consolidated import (was conversation_stats_updater)

# EDIT END

# Import Unified Data Loading System
from .components.unified_data_loader import UnifiedDataLoader
from .components.unified_load_button import get_unified_load_button_manager

logger = logging.getLogger(__name__)


class TheaMainWindow(QMainWindow):
    """Main window for Thea - Dreamscape MMORPG Platform."""

    def __init__(self):
        super().__init__()
        
        # Initialize loading manager first
        self.loading_manager = LoadingManager(self)
        self.loading_manager.show()
        
        # Initialize systems
        self.init_systems()
        
        # Initialize UI
        self.init_ui()
        
        # Initialize Unified Export Center
        self.unified_export_center = UnifiedExportCenter()
        
        # Hide loading screen
        self.loading_manager.hide()
        
        # Center window
        self.center_window()
        
        # Start background refresh timer
        self.start_background_refresh()

        # Initialize Unified Data Loading System
        self.unified_data_loader = UnifiedDataLoader(self)
        self.unified_data_loader.hide()  # Hidden by default
        
        # Setup global button manager
        self.button_manager = get_unified_load_button_manager()
        self.button_manager.set_data_loader(self.unified_data_loader)
        
        # Connect data loader signals
        self.unified_data_loader.operation_completed.connect(self.on_data_load_completed)
        self.unified_data_loader.cache_updated.connect(self.on_cache_updated)

    def init_systems(self):
        """Initialize core systems."""
        try:
            # Step 1: Initialize core systems
            self.loading_manager.next_step("Initializing core systems...")

            # Step 2: Database connections
            self.loading_manager.next_step("Loading database connections...")
            self.memory_manager = MemoryManager(str(MEMORY_DB_PATH))

            # Step 3: Memory management
            self.loading_manager.next_step("Setting up memory management...")

            # Step 4: MMORPG engine
            self.loading_manager.next_step("Initializing MMORPG engine...")
            self.mmorpg_engine = MMORPGEngine(str(MEMORY_DB_PATH))

            # Step 5: Discord integration
            self.loading_manager.next_step("Loading Discord integration...")
            self.discord_manager = DiscordManager()

            # Step 6: Scraping systems
            self.loading_manager.next_step("Setting up scraping systems...")
            self.scraping_manager = ScraperOrchestrator()

            # Step 7: Resume tracker
            self.loading_manager.next_step("Initializing resume tracking...")
            self.resume_tracker = ResumeTracker(str(RESUME_DB_PATH))

            # Step 8: Enhanced skill system
            self.enhanced_skill_system = EnhancedSkillResumeSystem(
                self.memory_manager, self.mmorpg_engine, self.resume_tracker
            )

            # Step 9: Load conversation data (with caching)
            self.loading_manager.next_step("Loading conversation data...")
            stats = self.memory_manager.get_conversation_stats()
            logger.info(
                f"Loaded conversation stats: {stats.get('total_conversations', 0)} conversations"
            )

            # Test MMORPG engine
            player_info = self.mmorpg_engine.get_player_info()
            logger.info(
                f"MMORPG engine test: Player={player_info.get('name', 'Unknown')}, Skills count={len(player_info.get('skills', []))}"
            )

            # Step 10: Initialize Unified Export Center
            self.loading_manager.next_step("Setting up unified export system...")
            self.unified_export_center = UnifiedExportCenter()

        except Exception as e:
            logger.error(f"Failed to initialize systems: {e}")
            QMessageBox.critical(
                self, "Initialization Error", f"Failed to initialize systems: {e}"
            )
            raise

    def init_ui(self):
        """Initialize the user interface."""
        try:
            # Step 11: Building user interface
            self.loading_manager.next_step("Building user interface...")

            # Set up main window
            self.setWindowTitle("Thea - Dreamscape MMORPG Platform")
            self.setMinimumSize(1400, 900)

            # Create central widget
            self.central_widget = QWidget()
            self.setCentralWidget(self.central_widget)

            # Create main layout (horizontal for sidebar + content)
            self.main_layout = QHBoxLayout(self.central_widget)
            self.main_layout.setContentsMargins(0, 0, 0, 0)
            self.main_layout.setSpacing(0)

            # Create sidebar
            self.create_sidebar()
            self.main_layout.addWidget(self.sidebar_frame)

            # Create main content area with stacked panels
            self.create_main_content()
            self.main_layout.addWidget(self.main_content)

            # Set stretch factors (sidebar: 0, main content: 1)
            self.main_layout.setStretch(0, 0)  # Sidebar doesn't stretch
            self.main_layout.setStretch(1, 1)  # Main content stretches

            # Set up connections
            self.setup_connections()

            # Load initial data
            self.load_initial_data()

            # Apply styling
            self.apply_styling()

            # Step 12: Finalizing startup
            self.loading_manager.next_step("Finalizing startup...")

        except Exception as e:
            logger.error(f"Failed to initialize UI: {e}")
            QMessageBox.critical(self, "UI Error", f"Failed to initialize UI: {e}")
            raise

    @debug_button("create_sidebar", "Main Window")
    def create_sidebar(self):
        """Create the sidebar navigation."""
        self.sidebar_frame = QFrame()
        self.sidebar_frame.setObjectName("sidebar")
        self.sidebar_frame.setMaximumWidth(250)
        self.sidebar_frame.setMinimumWidth(200)
        self.sidebar_frame.setFrameStyle(QFrame.Shape.StyledPanel)

        sidebar_layout = QVBoxLayout(self.sidebar_frame)
        sidebar_layout.setContentsMargins(10, 10, 10, 10)
        sidebar_layout.setSpacing(5)

        # Logo/Title
        title_label = QLabel("Thea")
        title_label.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sidebar_layout.addWidget(title_label)

        subtitle_label = QLabel("Dreamscape MMORPG")
        subtitle_label.setFont(QFont("Arial", 10))
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sidebar_layout.addWidget(subtitle_label)

        # Navigation buttons
        self.nav_buttons = {}
        nav_items = [
            ("🏠 Dashboard", "dashboard"),
            ("💬 Conversations", "conversations"),
            ("📝 Templates", "templates"),
            ("🔄 Workflows", "workflows"),
            ("⚔️ Combat Engine", "combat_engine"),
            ("⚔️ Memory Weaponization", "memory_weaponization"),
            ("🤖 AI Studio", "ai_studio"),
            ("🌳 Skill Tree", "skill_tree"),
            ("🎮 Gamification", "gamification"),
            ("📋 Quest Log", "tasks"),
            ("📄 Resume Studio", "resume_studio"),
            ("📊 Analytics & Export", "analytics_export"),
            ("📈 Content Analytics", "content_analytics"),
            ("🚀 Enhanced Analytics", "enhanced_analytics"),
            ("⚙️ Settings", "settings"),
        ]

        for text, key in nav_items:
            btn = QPushButton(text)
            btn.setCheckable(True)
            btn.setMinimumHeight(40)
            btn.setProperty("class", "nav")
            btn.clicked.connect(lambda checked, k=key: self.switch_panel(k))
            self.nav_buttons[key] = btn
            sidebar_layout.addWidget(btn)

        self.nav_buttons["dashboard"].setChecked(True)

        sidebar_layout.addStretch()

        # Player info
        self.player_info = QLabel("Loading player info...")
        self.player_info.setWordWrap(True)
        sidebar_layout.addWidget(self.player_info)

    @debug_button("_create_placeholder_panel", "Main Window")
    def _create_placeholder_panel(self, title: str) -> QWidget:
        """Return a simple QWidget with a large centered 'Coming Soon' message."""
        placeholder = QWidget()
        layout = QVBoxLayout(placeholder)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        suffix = " – Coming Soon" if "Discord" not in title else ""
        label = QLabel(f"{title}{suffix}")
        label.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)
        return placeholder

    @debug_button("create_main_content", "Main Window")
    def create_main_content(self):
        """Create the main content area with stacked panels."""
        self.main_content = QStackedWidget()
        self.panel_indices = {}

        def _add_panel(key: str, widget: QWidget):
            self.main_content.addWidget(widget)
            self.panel_indices[key] = self.main_content.count() - 1

        # Core implemented panels
        self.dashboard_panel = DashboardPanel()
        self.conversations_panel = ConversationsPanel()
        self.templates_panel = TemplatesPanel()
        self.workflow_panel = WorkflowPanel()

        # Consolidated panels
        from dreamscape.gui.panels.consolidated_memory_weaponization_panel import (
            MemoryWeaponizationPanel,
        )

        self.memory_weaponization_panel = MemoryWeaponizationPanel(
            memory_manager=self.memory_manager, mmorpg_engine=self.mmorpg_engine
        )

        from dreamscape.gui.panels.consolidated_ai_studio_panel import AIStudioPanel

        self.ai_studio_panel = AIStudioPanel(
            memory_manager=self.memory_manager, mmorpg_engine=self.mmorpg_engine
        )

        # Analytics Export Panel (optional - may fail if dependencies not available)
        try:
            from dreamscape.gui.panels.consolidated_analytics_export_panel import (
                AnalyticsExportPanel,
            )

            self.analytics_export_panel = AnalyticsExportPanel(
                memory_manager=self.memory_manager, mmorpg_engine=self.mmorpg_engine
            )
        except Exception as e:
            logger.warning(f"Analytics Export Panel not available: {e}")
            self.analytics_export_panel = self._create_placeholder_panel(
                "📊 Analytics Export - Not Available"
            )

        # Content Analytics Panel
        self.content_analytics_panel = ContentAnalyticsPanel()

        # Enhanced Analytics Panel
        self.enhanced_analytics_panel = EnhancedAnalyticsPanel()

        # Combat Engine Panel
        self.combat_engine_panel = CombatEnginePanel(self)

        _add_panel("dashboard", self.dashboard_panel)
        _add_panel("conversations", self.conversations_panel)
        _add_panel("templates", self.templates_panel)
        _add_panel("workflows", self.workflow_panel)
        _add_panel("memory_weaponization", self.memory_weaponization_panel)
        _add_panel("ai_studio", self.ai_studio_panel)
        _add_panel("analytics_export", self.analytics_export_panel)
        _add_panel("content_analytics", self.content_analytics_panel)
        _add_panel("enhanced_analytics", self.enhanced_analytics_panel)
        _add_panel("combat_engine", self.combat_engine_panel)

        # Quest Log panel
        self.quest_log_panel = QuestLogPanel(self.mmorpg_engine)
        _add_panel("tasks", self.quest_log_panel)

        # Resume Studio panel (consolidated resume functionality)
        from dreamscape.gui.panels.resume_panel import ResumePanel

        self.resume_panel = ResumePanel(
            memory_manager=self.memory_manager, resume_tracker=self.resume_tracker
        )
        _add_panel("resume_studio", self.resume_panel)

        # Discord panel (devlog functionality moved to AI Studio)
        self.discord_panel = QWidget()  # Placeholder for future Discord integration
        _add_panel("discord", self.discord_panel)

        # Settings panel
        self.settings_panel = SettingsPanel()
        _add_panel("settings", self.settings_panel)

        # Skill Tree panel
        self.skill_tree_panel = SkillTreePanel(
            memory_manager=self.memory_manager, mmorpg_engine=self.mmorpg_engine
        )
        _add_panel("skill_tree", self.skill_tree_panel)

        # Gamification panel
        self.gamification_panel = GamificationPanel()
        _add_panel("gamification", self.gamification_panel)

        # Set dashboard as default
        self.main_content.setCurrentIndex(self.panel_indices["dashboard"])

    @debug_button("add_placeholder_panels", "Main Window")
    def add_placeholder_panels(self):
        """Add placeholder panels for unimplemented sections."""
        placeholder_texts = [
            "📄 Resume - Coming Soon",
            "📊 Analytics - Coming Soon",
            "📤 Export - Coming Soon",
            "📢 Discord/Devlog",
        ]

        for text in placeholder_texts:
            placeholder = QWidget()
            layout = QVBoxLayout(placeholder)
            label = QLabel(text)
            label.setFont(QFont("Arial", 16))
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(label)
            self.main_content.addWidget(placeholder)

    @debug_button("setup_connections", "Main Window")
    def setup_connections(self):
        """Set up signal connections."""
        try:
            # Connect dashboard refresh button to main window update method
            self.dashboard_panel.refresh_btn.clicked.disconnect()  # Disconnect existing connection
            self.dashboard_panel.refresh_btn.clicked.connect(
                self.refresh_dashboard_data
            )

            # Note: refresh_requested signal connection removed as it's not emitted by DashboardPanel

            # Connect quick ingestion button
            self.dashboard_panel.quick_ingest_btn.clicked.connect(
                self.dashboard_panel.quick_ingestion_and_progress
            )

            # Connect conversations panel signals
            self.conversations_panel.refresh_requested.connect(
                self.refresh_conversations
            )
            self.conversations_panel.import_requested.connect(
                self.import_new_conversations
            )
            self.conversations_panel.process_conversations_requested.connect(
                self.process_conversations
            )
            self.conversations_panel.update_statistics_requested.connect(
                self.update_conversation_statistics
            )

            # Connect main content stack change to load conversations when panel is shown
            self.main_content.currentChanged.connect(self._on_stack_changed)

            # EDIT START: Connect TemplatesPanel.template_applied for global template selection
            self.templates_panel.template_applied.connect(self._on_template_applied)
            # EDIT END

        except Exception as e:
            logger.error(f"Failed to setup connections: {e}")

    @debug_button("load_initial_data", "Main Window")
    def load_initial_data(self):
        """Load initial data for the application."""
        try:
            # Refresh dashboard data
            self.refresh_dashboard_data()

            # Load conversations in background
            from threading import Thread

            Thread(target=self._load_conversations_background, daemon=True).start()

        except Exception as e:
            logger.error(f"Failed to load initial data: {e}")

    @debug_button("_load_conversations_background", "Main Window")
    def _load_conversations_background(self):
        """Load conversations in background thread."""
        try:
            self.conversations_panel.load_all_conversations()
            logger.info("Conversations loaded in background")
        except Exception as e:
            logger.error(f"Failed to load conversations in background: {e}")

    @debug_button("start_background_refresh", "Main Window")
    def start_background_refresh(self):
        """Start background refresh timer."""
        try:
            # Refresh data every 30 seconds
            self.refresh_timer = QTimer()
            self.refresh_timer.timeout.connect(self.background_refresh)
            self.refresh_timer.start(30000)  # 30 seconds

        except Exception as e:
            logger.error(f"Failed to start background refresh: {e}")

    @debug_button("background_refresh", "Main Window")
    def background_refresh(self):
        """Background refresh of data."""
        try:
            # Refresh dashboard data in background
            self.refresh_dashboard_data()

        except Exception as e:
            logger.error(f"Background refresh failed: {e}")

    @debug_button("refresh_dashboard_data", "Main Window")
    def refresh_dashboard_data(self, *args, **kwargs):
        """Refresh dashboard data."""
        try:
            # Clear conversation stats cache to force fresh data
            if hasattr(self.memory_manager, "storage") and hasattr(
                self.memory_manager.storage, "stats_cache"
            ):
                self.memory_manager.storage.stats_cache.clear_cache("conversations")

            # Get conversation stats (now fresh from cache clear)
            stats = self.memory_manager.get_conversation_stats()

            # Update dashboard with new stats
            if hasattr(self, "dashboard_panel"):
                self.dashboard_panel.update_stats(stats)

            # Update status bar
            self.statusBar().showMessage(
                f"Ready - {stats.get('total_conversations', 0)} conversations"
            )

        except Exception as e:
            logger.error(f"Failed to refresh dashboard data: {e}")

    @debug_button("refresh_chatgpt_conversation_history", "Main Window")
    def refresh_chatgpt_conversation_history(self):
        """Handle ChatGPT conversation history refresh from dashboard."""
        try:
            # This will be called by the dashboard panel's ChatGPT refresh button
            # The actual refresh logic is in the dashboard panel
            logger.info("ChatGPT conversation history refresh requested from dashboard")

            # Update status bar to show refresh is in progress
            self.statusBar().showMessage("Refreshing ChatGPT conversation history...")

        except Exception as e:
            logger.error(f"Failed to handle ChatGPT refresh request: {e}")
            self.show_error(f"Failed to handle ChatGPT refresh request: {e}")

    def show(self):
        """Show the main window."""
        super().show()
        # Center the window
        self.center_window()

    def center_window(self):
        """Center the window on the screen."""
        screen = QApplication.primaryScreen().geometry()
        size = self.geometry()
        x = (screen.width() - size.width()) // 2
        y = (screen.height() - size.height()) // 2
        self.move(x, y)

    def switch_panel(self, panel_name: str):
        """Switch to a different panel using the dynamic index map."""
        if hasattr(self, "panel_indices") and panel_name in self.panel_indices:
            self.main_content.setCurrentIndex(self.panel_indices[panel_name])
            for key, btn in self.nav_buttons.items():
                btn.setChecked(key == panel_name)
        else:
            logger.warning(f"Panel '{panel_name}' not available in stack")

    @debug_button("load_templates", "Main Window")
    def load_templates(self):
        """Load templates from the database and templates/ directory."""
        try:
            # --------------------------- DB templates ---------------------------
            templates = self.memory_manager.get_templates()  # returns list[dict]
            ui_templates = [
                {
                    "id": t.get("id"),
                    "name": t.get("name"),
                    "content": t.get("template_content"),
                    "description": t.get("description"),
                    "category": t.get("category") or "database",
                    "source": "database",
                }
                for t in templates
            ]

            # ------------------------- File-system templates -------------------
            from pathlib import Path

            templates_dir = Path(__file__).parent.parent / "templates"
            if templates_dir.exists():
                for ext in ("*.j2", "*.md"):
                    for path in templates_dir.rglob(ext):
                        try:
                            content = path.read_text(encoding="utf-8")
                        except Exception:
                            continue  # Skip unreadable files
                        rel_path = path.relative_to(templates_dir).as_posix()
                        name = path.stem
                        # Skip if a DB template with same name already exists
                        if any(t["name"] == name for t in ui_templates):
                            continue
                        ui_templates.append(
                            {
                                "id": rel_path,
                                "name": name,
                                "content": content,
                                "description": f"File template ({rel_path})",
                                "category": path.parent.name,
                                "source": "file",
                            }
                        )

            # -------------------------------------------------------------------
            if not ui_templates:
                self.statusBar().showMessage("No templates found", 5000)
            self.templates_panel.load_templates(ui_templates)
        except Exception as e:
            self.show_error(f"Failed to load templates: {e}")

    @debug_button("update_dashboard", "Main Window")
    def update_dashboard(self):
        """Update the dashboard with current data."""
        try:
            # Get player info
            player = self.mmorpg_engine.get_player()
            self.dashboard_panel.update_player_info(player)

            # Get skills
            skills = self.mmorpg_engine.get_skills()
            logger.debug(f"Skills type: {type(skills)}, Skills value: {skills}")
            self.dashboard_panel.update_skills(skills)

            # Get game stats
            game_stats = self.mmorpg_engine.get_game_status()
            self.dashboard_panel.update_stats(game_stats)

            # Update player info in sidebar
            self.player_info.setText(
                f"{player.name}\n{player.architect_tier}\n{player.xp} XP"
            )

            # Check live processor status
            self.dashboard_panel.check_live_processor_status()

        except Exception as e:
            logger.error(f"Failed to update dashboard: {e}")
            self.show_error(f"Failed to update dashboard: {e}")

    def on_conversation_selected(self, conversation):
        pass

    @debug_button("on_template_saved", "Main Window")
    def on_template_saved(self, template):
        self.statusBar().showMessage(
            f"Template '{template.get('name', 'Unknown')}' saved"
        )

    @debug_button("on_template_deleted", "Main Window")
    def on_template_deleted(self, template_name):
        self.statusBar().showMessage(f"Template '{template_name}' deleted")

    @debug_button("on_settings_saved", "Main Window")
    def on_settings_saved(self, settings):
        self.statusBar().showMessage("Settings saved successfully")
        # Apply new styling in case theme or accessibility options changed
        self.apply_styling()

    def apply_styling(self):
        """Apply modern styling to the application."""
        # Get current theme from settings
        theme = self.get_current_theme()
        self.apply_theme(theme)

    def get_current_theme(self) -> str:
        """Get the current theme setting."""
        return settings_manager.get_theme()

    def apply_theme(self, theme: str):
        """Apply a specific theme to the application."""
        if settings_manager.get_setting("high_contrast", False):
            self.apply_high_contrast_theme()
            return
        if theme == "Dark":
            self.apply_dark_theme()
        elif theme == "Light":
            self.apply_light_theme()
        else:  # System theme
            self.apply_system_theme()

    def apply_dark_theme(self):
        """Apply dark theme styling."""
        self.setStyleSheet(
            """
            /* Main Window */
            QMainWindow { 
                background-color: #1e1e1e; 
                color: #ffffff;
            }
            
            /* Sidebar */
            QFrame#sidebar { 
                background-color: #252526; 
                border: 1px solid #3e3e42; 
                border-radius: 5px; 
            }
            
            /* Buttons */
            QPushButton { 
                background-color: #0e639c; 
                color: white; 
                border: none; 
                padding: 8px 16px; 
                border-radius: 4px; 
                font-weight: bold; 
            }
            QPushButton:hover { 
                background-color: #1177bb; 
            }
            QPushButton:pressed { 
                background-color: #0c5a8b; 
            }
            QPushButton:checked { 
                background-color: #1177bb; 
            }
            QPushButton:disabled {
                background-color: #3e3e42;
                color: #6a6a6a;
            }
            
            /* Navigation buttons */
            QPushButton[class="nav"] {
                background-color: transparent;
                color: #cccccc;
                text-align: left;
                padding: 10px 15px;
                border-radius: 0px;
                font-weight: normal;
            }
            QPushButton[class="nav"]:hover {
                background-color: #2a2d2e;
            }
            QPushButton[class="nav"]:checked {
                background-color: #37373d;
                color: #ffffff;
            }
            
            /* Labels */
            QLabel { 
                color: #cccccc; 
            }
            
            /* Group boxes */
            QGroupBox { 
                font-weight: bold; 
                border: 2px solid #3e3e42; 
                border-radius: 5px; 
                margin-top: 1ex; 
                padding-top: 10px; 
                color: #cccccc;
            }
            QGroupBox::title { 
                subcontrol-origin: margin; 
                left: 10px; 
                padding: 0 5px 0 5px; 
                color: #cccccc;
            }
            
            /* Tables */
            QTableWidget {
                background-color: #252526;
                alternate-background-color: #2d2d30;
                color: #cccccc;
                gridline-color: #3e3e42;
                border: 1px solid #3e3e42;
            }
            QTableWidget::item {
                padding: 5px;
            }
            QTableWidget::item:selected {
                background-color: #094771;
                color: #ffffff;
            }
            QHeaderView::section {
                background-color: #2d2d30;
                color: #cccccc;
                padding: 5px;
                border: 1px solid #3e3e42;
                font-weight: bold;
            }
            
            /* Text areas */
            QTextEdit, QPlainTextEdit {
                background-color: #1e1e1e;
                color: #cccccc;
                border: 1px solid #3e3e42;
                border-radius: 4px;
            }
            
            /* Line edits */
            QLineEdit {
                background-color: #3c3c3c;
                color: #cccccc;
                border: 1px solid #3e3e42;
                border-radius: 4px;
                padding: 5px;
            }
            QLineEdit:focus {
                border: 1px solid #007acc;
            }
            
            /* Combo boxes */
            QComboBox {
                background-color: #3c3c3c;
                color: #cccccc;
                border: 1px solid #3e3e42;
                border-radius: 4px;
                padding: 5px;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #cccccc;
            }
            QComboBox QAbstractItemView {
                background-color: #3c3c3c;
                color: #cccccc;
                border: 1px solid #3e3e42;
                selection-background-color: #094771;
            }
            
            /* Spin boxes */
            QSpinBox {
                background-color: #3c3c3c;
                color: #cccccc;
                border: 1px solid #3e3e42;
                border-radius: 4px;
                padding: 5px;
            }
            
            /* Check boxes */
            QCheckBox {
                color: #cccccc;
            }
            QCheckBox::indicator {
                width: 16px;
                height: 16px;
                border: 1px solid #3e3e42;
                border-radius: 3px;
                background-color: #3c3c3c;
            }
            QCheckBox::indicator:checked {
                background-color: #007acc;
                border: 1px solid #007acc;
            }
            
            /* Tab widget */
            QTabWidget::pane {
                border: 1px solid #3e3e42;
                background-color: #252526;
            }
            QTabBar::tab {
                background-color: #2d2d30;
                color: #cccccc;
                padding: 8px 16px;
                border: 1px solid #3e3e42;
                border-bottom: none;
            }
            QTabBar::tab:selected {
                background-color: #252526;
                color: #ffffff;
            }
            QTabBar::tab:hover {
                background-color: #3e3e42;
            }
            
            /* Scroll bars */
            QScrollBar:vertical {
                background-color: #2d2d30;
                width: 12px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical {
                background-color: #3e3e42;
                border-radius: 6px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #4e4e52;
            }
            
            /* Progress bars */
            QProgressBar {
                border: 1px solid #3e3e42;
                border-radius: 4px;
                text-align: center;
                background-color: #2d2d30;
                color: #cccccc;
            }
            QProgressBar::chunk {
                background-color: #007acc;
                border-radius: 3px;
            }
            
            /* Status bar */
            QStatusBar {
                background-color: #007acc;
                color: #ffffff;
            }
            
            /* Menu bar */
            QMenuBar {
                background-color: #2d2d30;
                color: #cccccc;
                border-bottom: 1px solid #3e3e42;
            }
            QMenuBar::item {
                background-color: transparent;
                padding: 5px 10px;
            }
            QMenuBar::item:selected {
                background-color: #3e3e42;
            }
            QMenu {
                background-color: #2d2d30;
                color: #cccccc;
                border: 1px solid #3e3e42;
            }
            QMenu::item:selected {
                background-color: #094771;
            }
        """
        )

    def apply_light_theme(self):
        """Apply light theme styling."""
        self.setStyleSheet(
            """
            /* Main Window */
            QMainWindow { 
                background-color: #f5f5f5; 
                color: #333333;
            }
            
            /* Sidebar */
            QFrame#sidebar { 
                background-color: #ffffff; 
                border: 1px solid #ddd; 
                border-radius: 5px; 
            }
            
            /* Buttons */
            QPushButton { 
                background-color: #0078d4; 
                color: white; 
                border: none; 
                padding: 8px 16px; 
                border-radius: 4px; 
                font-weight: bold; 
            }
            QPushButton:hover { 
                background-color: #106ebe; 
            }
            QPushButton:pressed { 
                background-color: #005a9e; 
            }
            QPushButton:checked { 
                background-color: #106ebe; 
            }
            QPushButton:disabled {
                background-color: #cccccc;
                color: #666666;
            }
            
            /* Navigation buttons */
            QPushButton[class="nav"] {
                background-color: transparent;
                color: #333333;
                text-align: left;
                padding: 10px 15px;
                border-radius: 0px;
                font-weight: normal;
            }
            QPushButton[class="nav"]:hover {
                background-color: #f0f0f0;
            }
            QPushButton[class="nav"]:checked {
                background-color: #e1f5fe;
                color: #0078d4;
            }
            
            /* Labels */
            QLabel { 
                color: #333333; 
            }
            
            /* Group boxes */
            QGroupBox { 
                font-weight: bold; 
                border: 2px solid #ddd; 
                border-radius: 5px; 
                margin-top: 1ex; 
                padding-top: 10px; 
                color: #333333;
            }
            QGroupBox::title { 
                subcontrol-origin: margin; 
                left: 10px; 
                padding: 0 5px 0 5px; 
                color: #333333;
            }
            
            /* Tables */
            QTableWidget {
                background-color: #ffffff;
                alternate-background-color: #f9f9f9;
                color: #333333;
                gridline-color: #ddd;
                border: 1px solid #ddd;
            }
            QTableWidget::item {
                padding: 5px;
            }
            QTableWidget::item:selected {
                background-color: #0078d4;
                color: #ffffff;
            }
            QHeaderView::section {
                background-color: #f5f5f5;
                color: #333333;
                padding: 5px;
                border: 1px solid #ddd;
                font-weight: bold;
            }
            
            /* Text areas */
            QTextEdit, QPlainTextEdit {
                background-color: #ffffff;
                color: #333333;
                border: 1px solid #ddd;
                border-radius: 4px;
            }
            
            /* Line edits */
            QLineEdit {
                background-color: #ffffff;
                color: #333333;
                border: 1px solid #ddd;
                border-radius: 4px;
                padding: 5px;
            }
            QLineEdit:focus {
                border: 1px solid #0078d4;
            }
            
            /* Combo boxes */
            QComboBox {
                background-color: #ffffff;
                color: #333333;
                border: 1px solid #ddd;
                border-radius: 4px;
                padding: 5px;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #333333;
            }
            QComboBox QAbstractItemView {
                background-color: #ffffff;
                color: #333333;
                border: 1px solid #ddd;
                selection-background-color: #0078d4;
            }
            
            /* Spin boxes */
            QSpinBox {
                background-color: #ffffff;
                color: #333333;
                border: 1px solid #ddd;
                border-radius: 4px;
                padding: 5px;
            }
            
            /* Check boxes */
            QCheckBox {
                color: #333333;
            }
            QCheckBox::indicator {
                width: 16px;
                height: 16px;
                border: 1px solid #ddd;
                border-radius: 3px;
                background-color: #ffffff;
            }
            QCheckBox::indicator:checked {
                background-color: #0078d4;
                border: 1px solid #0078d4;
            }
            
            /* Tab widget */
            QTabWidget::pane {
                border: 1px solid #ddd;
                background-color: #ffffff;
            }
            QTabBar::tab {
                background-color: #f5f5f5;
                color: #333333;
                padding: 8px 16px;
                border: 1px solid #ddd;
                border-bottom: none;
            }
            QTabBar::tab:selected {
                background-color: #ffffff;
                color: #0078d4;
            }
            QTabBar::tab:hover {
                background-color: #e9e9e9;
            }
            
            /* Scroll bars */
            QScrollBar:vertical {
                background-color: #f5f5f5;
                width: 12px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical {
                background-color: #c1c1c1;
                border-radius: 6px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #a8a8a8;
            }
            
            /* Progress bars */
            QProgressBar {
                border: 1px solid #ddd;
                border-radius: 4px;
                text-align: center;
                background-color: #f5f5f5;
                color: #333333;
            }
            QProgressBar::chunk {
                background-color: #0078d4;
                border-radius: 3px;
            }
            
            /* Status bar */
            QStatusBar {
                background-color: #0078d4;
                color: #ffffff;
            }
            
            /* Menu bar */
            QMenuBar {
                background-color: #f5f5f5;
                color: #333333;
                border-bottom: 1px solid #ddd;
            }
            QMenuBar::item {
                background-color: transparent;
                padding: 5px 10px;
            }
            QMenuBar::item:selected {
                background-color: #e9e9e9;
            }
            QMenu {
                background-color: #ffffff;
                color: #333333;
                border: 1px solid #ddd;
            }
            QMenu::item:selected {
                background-color: #0078d4;
                color: #ffffff;
            }
        """
        )

    def apply_high_contrast_theme(self):
        """Apply high contrast styling for accessibility."""
        self.setStyleSheet(
            """
            QMainWindow {
                background-color: #000000;
                color: #ffffff;
            }
            QPushButton {
                background-color: #000000;
                color: #ffffff;
                border: 1px solid #ffffff;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background-color: #222222;
            }
            QLabel { color: #ffffff; }
        """
        )

    def apply_system_theme(self):
        """Apply system theme (follows OS theme)."""
        # EDIT START: OS theme detection for 'System' mode
        import sys

        is_dark = False
        if sys.platform == "win32":
            try:
                import winreg

                registry = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
                key = winreg.OpenKey(
                    registry,
                    r"Software\\Microsoft\\Windows\\CurrentVersion\\Themes\\Personalize",
                )
                value, _ = winreg.QueryValueEx(key, "AppsUseLightTheme")
                is_dark = value == 0  # 0 = dark, 1 = light
            except Exception as e:
                # Fallback to light if detection fails
                is_dark = False
        elif sys.platform == "darwin":
<<<<<<< HEAD
            # macOS dark mode detection
            try:
                import subprocess

                # Use defaults command to check macOS appearance
                result = subprocess.run(
                    ['defaults', 'read', '-g', 'AppleInterfaceStyle'],
                    capture_output=True,
                    text=True,
                    timeout=5
                )

                # If command succeeds and returns "Dark", system is in dark mode
                is_dark = result.returncode == 0 and result.stdout.strip() == "Dark"

                logger.info(f"macOS dark mode detection: {'enabled' if is_dark else 'disabled'}")

            except (subprocess.TimeoutExpired, subprocess.SubprocessError, FileNotFoundError) as e:
                logger.warning(f"macOS dark mode detection failed: {e}")
                # Fallback: try alternative method using NSAppearance if available
                try:
                    # This is a more advanced method that would require PyObjC
                    # For now, fallback to light theme
                    is_dark = False
                except Exception:
                    is_dark = False
=======
            # TODO: Implement macOS dark mode detection
            # For now, fallback to light
            is_dark = False
>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1
        else:
            # TODO: Implement Linux/other OS dark mode detection
            # For now, fallback to light
            is_dark = False
        if is_dark:
            self.apply_dark_theme()
        else:
            self.apply_light_theme()
        # EDIT END: OS theme detection for 'System' mode

    def switch_theme(self, theme: str):
        """Switch to a specific theme."""
        settings_manager.set_theme(theme)
        self.apply_theme(theme)

    def show_error(self, message: str):
        """Show an error message."""
        QMessageBox.critical(self, "Error", message)
        self.statusBar().showMessage(f"Error: {message}")

    def _handle_scraper_event(self, event_type: str, data: Any):
        """Handle events from the scraper panel."""
        if event_type == "conversations_extracted":
            # AI Interaction panel disabled; placeholder for future integration
            pass

        # ... existing event handling code ...

    @debug_button("_on_stack_changed", "Main Window")
    def _on_stack_changed(self, index: int):
        # If analytics panel is shown, refresh its data using unified stats updater
        if hasattr(self, "analytics_panel") and index == self.panel_indices.get(
            "analytics"
        ):
            try:
                stats = ConversationStatsUpdater(
                    self.memory_manager
                ).get_conversation_stats_summary(trend=True)
                self.analytics_panel.update_overview(stats)
            except Exception as e:
                logger.warning(f"Failed to refresh analytics: {e}")

        # If dashboard panel is shown, refresh its data with comprehensive stats
        if hasattr(self, "dashboard_panel") and index == self.panel_indices.get(
            "dashboard"
        ):
            try:
                self.refresh_dashboard_data()
            except Exception as e:
                logger.warning(f"Failed to refresh dashboard: {e}")

        # If conversations panel is shown, load conversations
        if hasattr(self, "conversations_panel") and index == self.panel_indices.get(
            "conversations"
        ):
            try:
                self.conversations_panel.load_all_conversations()
            except Exception as e:
                logger.warning(f"Failed to load conversations: {e}")

    @debug_button("refresh_conversations", "Main Window")
    def refresh_conversations(self):
        """Refresh the conversations panel and status bar."""
        try:
            self.conversations_panel.load_all_conversations()
            self.statusBar().showMessage("Conversations refreshed", 3000)
        except Exception as e:
            self.show_error(f"Failed to refresh conversations: {e}")

    @debug_button("process_conversations", "Main Window")
    def process_conversations(self):
        """Process conversations for Dreamscape analysis."""
        try:
            from threading import Thread

            self.statusBar().showMessage(
                "Processing conversations for Dreamscape analysis...", 0
            )

            def _process():
                try:
                    # This would trigger the enhanced skill system and MMORPG updates
                    enhanced_system = EnhancedSkillResumeSystem(
                        self.memory_manager, self.mmorpg_engine, self.resume_tracker
                    )
                    skill_tree = enhanced_system.build_enhanced_skill_tree()

                    # Update MMORPG progress based on conversations
                    conversations = self.memory_manager.get_recent_conversations(
                        limit=1000
                    )
                    for conversation in conversations:
                        try:
                            self.mmorpg_engine.update_from_conversation(
                                conversation["id"]
                            )
                        except Exception as e:
                            logger.warning(
                                f"Failed to update MMORPG from conversation {conversation.get('id', 'unknown')}: {e}"
                            )

                    self.statusBar().showMessage(
                        "Dreamscape processing completed!", 5000
                    )
                except Exception as e:
                    logger.error(f"Dreamscape processing failed: {e}")
                    self.statusBar().showMessage(
                        f"Dreamscape processing failed: {e}", 5000
                    )

            Thread(target=_process, daemon=True).start()

        except Exception as e:
            logger.error(f"Failed to start conversation processing: {e}")
            self.show_error(f"Failed to start conversation processing: {e}")

    @debug_button("update_conversation_statistics", "Main Window")
    def update_conversation_statistics(self):
        """Update conversation statistics."""
        try:
            # Refresh conversation stats in memory manager
            stats = self.memory_manager.get_conversation_stats()

            # Update dashboard with new stats
            if hasattr(self, "dashboard_panel"):
                self.dashboard_panel.update_stats(stats)

            # Update status bar
            self.statusBar().showMessage(
                f"Statistics updated - {stats.get('total_conversations', 0)} conversations",
                3000,
            )

        except Exception as e:
            logger.error(f"Failed to update conversation statistics: {e}")
            self.show_error(f"Failed to update conversation statistics: {e}")

    @debug_button("import_new_conversations", "Main Window")
    def import_new_conversations(self):
        """Ingest new JSONs from data/conversations without blocking the UI."""
        from threading import Thread
        import traceback

        def _run_ingest():
            try:
                ingested = self.memory_manager.ingest_conversations(
                    "data/conversations"
                )
                self.statusBar().showMessage(
                    f"📥 Imported {ingested} new conversation files", 7000
                )
                if ingested:
                    # Reload table on main thread
                    self.conversations_panel.load_all_conversations()
            except Exception as e:
                logger.error(f"Manual import failed: {e}\n{traceback.format_exc()}")
                self.show_error(f"Failed to import conversations: {e}")

        Thread(target=_run_ingest, daemon=True).start()

    def _handle_template_action(self, payload: dict):
        """Handle actions coming from TemplatesPanel (edit or send).

        Enhanced: If OpenAI API key is not configured (or sending method
        is explicitly set to 'scraper' in settings), fall back to the
        Selenium-based ChatGPT web-scraper for prompt dispatch. This keeps
        prior async-API flow intact while enabling the requested
        webscraper implementation.
        """
        if payload.get("action") == "send":
            templates = payload.get("templates", [])
            if not templates:
                return

            # Which channel?  settings.json -> prompt_send_method: "api"|"scraper"
            send_method = settings_manager.get_setting("prompt_send_method", "api")

            # ------------------------------------------------------------------
            # 1) Try the OpenAI API path when selected and configured
            # ------------------------------------------------------------------
            async def _try_api():
                from dreamscape.core.chatgpt_api_client import ChatGPTAPIClient

                async with ChatGPTAPIClient() as client:
                    if not client.is_configured():
                        return False
                    for tmpl in templates:
                        await client.send_message("new", tmpl["content"])
                return True

            # ------------------------------------------------------------------
            # 2) Web-scraper fallback using Selenium
            # ------------------------------------------------------------------
            def _run_scraper_blocking():
                """Blocking helper executed in a worker thread."""
                from dreamscape.scrapers.chatgpt_scraper import ChatGPTScraper
                import traceback, logging

                try:
                    with ChatGPTScraper(headless=False, timeout=30) as scraper:
                        if not scraper.ensure_login():
                            logging.error("Scraper login failed")
                            return False
                        for tmpl in templates:
                            if not scraper.send_prompt(
                                tmpl["content"], wait_for_response=True
                            ):
                                logging.warning(
                                    "Failed to send prompt via scraper for template %s",
                                    tmpl.get("name"),
                                )
                    return True
                except Exception as exc:
                    logging.error(
                        "Scraper exception: %s\n%s", exc, traceback.format_exc()
                    )
                    return False

            # --------------------------------------------------------------
            # Dispatch according to preference with automatic fallback
            # --------------------------------------------------------------
            from threading import Thread
            import asyncio

            if send_method == "api":
                # Kick off API attempt; if it fails we chain scraper fallback
                async def _run_with_fallback():
                    ok = await _try_api()
                    if ok:
                        self.statusBar().showMessage(
                            f"Sent {len(templates)} prompt(s) to ChatGPT via API", 5000
                        )
                        return
                    # API path unavailable – revert to scraper
                    self.statusBar().showMessage(
                        "API not configured – using web interface", 3000
                    )

                    def _thread_target():
                        if _run_scraper_blocking():
                            self.statusBar().showMessage(
                                f"Sent {len(templates)} prompt(s) via web interface",
                                5000,
                            )
                        else:
                            self.show_error("Failed to send prompts via scraper")

                    Thread(target=_thread_target, daemon=True).start()

                asyncio.create_task(_run_with_fallback())
            else:
                # Directly use the scraper path (non-blocking via thread)
                def _thread_target():
                    if _run_scraper_blocking():
                        self.statusBar().showMessage(
                            f"Sent {len(templates)} prompt(s) via web interface", 5000
                        )
                    else:
                        self.show_error("Failed to send prompts via scraper")

                Thread(target=_thread_target, daemon=True).start()
        else:
            # Editing selection handled internally already
            pass

    def on_weaponization_completed(self, results: dict):
        """Handle weaponization completion."""
        self.statusBar().showMessage("Weaponization completed successfully!", 10000)
        logger.info(f"Weaponization completed: {results}")

        # Update dashboard to reflect new weaponized data
        self.refresh_dashboard_data()

        # Show completion message
        QMessageBox.information(
            self,
            "Weaponization Complete",
            "Your conversation corpus has been successfully weaponized!\n\n"
            "New capabilities available:\n"
            "• Vector search for instant context injection\n"
            "• Training datasets for AI model fine-tuning\n"
            "• MMORPG episodes from real conversations\n"
            "• Analytics dashboard for strategic insights\n"
            "• Content generation for monetization\n"
            "• REST API for external integration",
        )

    def on_weaponization_failed(self, error: str):
        """Handle weaponization failure."""
        self.statusBar().showMessage(f"Weaponization failed: {error}", 10000)
        logger.error(f"Weaponization failed: {error}")

        QMessageBox.critical(
            self,
            "Weaponization Failed",
            f"Weaponization operation failed:\n\n{error}\n\n"
            "Please check the logs for more details.",
        )

    def _on_agent_trained(self, result: dict):
        """Handle agent training completion."""
        try:
            # Update status
            agent_name = result.get("agent_config", {}).get("name", "Unknown Agent")
            self.statusBar().showMessage(
                f"Agent '{agent_name}' trained successfully!", 5000
            )

            # Refresh skill tree if it's currently visible
            if hasattr(self, "skill_tree_panel"):
                self.skill_tree_panel.refresh_data()

            # Show notification
            QMessageBox.information(
                self,
                "Agent Training Complete",
                f"Agent '{agent_name}' has been trained successfully!\n\n"
                f"Processed {result.get('conversations_processed', 0)} conversations\n"
                f"Generated {result.get('training_examples', 0)} training examples\n\n"
                f"The agent is now ready to assist you with personalized responses!",
            )

        except Exception as e:
            self.show_error(f"Failed to handle agent training completion: {e}")

    def _on_skill_selected(self, skill_data: dict):
        """Handle skill selection in skill tree."""
        try:
            skill_name = skill_data.get("name", "Unknown Skill")
            level = skill_data.get("level", 1)
            xp = skill_data.get("xp", 0)

            # Update status
            self.statusBar().showMessage(
                f"Selected skill: {skill_name} (Level {level}, {xp} XP)", 3000
            )

            # You could add more functionality here, such as:
            # - Showing skill details in a tooltip
            # - Highlighting related quests
            # - Suggesting next steps for skill progression

        except Exception as e:
            self.show_error(f"Failed to handle skill selection: {e}")

    def run_end_to_end_workflow(self, mode: str = "batch"):
        """Run the complete end-to-end workflow for processing conversations."""
        from threading import Thread
        import asyncio
        from PyQt6.QtCore import QTimer

        def _run_workflow():
            try:
                # Import the workflow
                import sys

                sys.path.insert(0, "scripts")
                from end_to_end_workflow import EndToEndWorkflow

                # Create workflow instance
                workflow = EndToEndWorkflow()

                # Run the workflow
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)

                try:
                    # Run the appropriate workflow based on mode
                    if mode == "batch":
                        results = loop.run_until_complete(
                            workflow.run_conversation_analysis_workflow()
                        )
                    elif mode == "preview":
                        results = loop.run_until_complete(
                            workflow.run_comprehensive_preview_workflow()
                        )
                    else:
                        results = loop.run_until_complete(
                            workflow.run_conversation_analysis_workflow()
                        )

                    # Schedule UI updates on the main thread
                    def update_ui():
                        try:
                            # Update status bar
                            successful = 1 if results.get("status") == "completed" else 0
                            total = 1

                            self.statusBar().showMessage(
                                f"🎉 End-to-end workflow completed: {successful}/{total} conversations processed",
                                10000,
                            )

                            # Show completion dialog with mode-specific content
                            workflow_status = results.get("status", "unknown")
                            
                            if mode == "preview":
                                # Handle preview workflow results
                                features_showcased = len(results.get("features_showcased", []))
                                user_variables = len(results.get("user_variables", {}))
                                setup_issues = len(results.get("user_variables", {}).get("setup_issues_resolved", []))
                                
                                # Get comprehensive report for additional details
                                report = results.get("comprehensive_report", {})
                                success_rate = report.get("success_rate", 0)
                                system_health = report.get("setup_analysis", {}).get("system_health", "Good")
                                
                                message = f"🎉 Preview workflow completed!\n\n"
                                message += f"📊 Preview Results:\n"
                                message += f"• Status: {workflow_status}\n"
                                message += f"• Features Showcased: {features_showcased}\n"
                                message += f"• User Variables Collected: {user_variables}\n"
                                message += f"• Success Rate: {success_rate:.1f}%\n"
                                message += f"• Processing Mode: Preview (5 conversations max)\n\n"
                                
                                if setup_issues > 0:
                                    message += f"🔧 Setup Assistance:\n"
                                    message += f"• Auto-resolved {setup_issues} setup issues\n"
                                    message += f"• System Health: {system_health}\n\n"
                                
                                message += f"🎭 All Dreamscape features have been demonstrated!\n"
                                message += f"🔄 Refresh dashboard to see updated stats!"
                                
                                QMessageBox.information(
                                    self,
                                    "🎭 Comprehensive Preview Complete",
                                    message,
                                )
                            else:
                                # Handle regular workflow results
                                steps_completed = len(results.get("steps_completed", []))
                                errors = len(results.get("errors", []))

                                QMessageBox.information(
                                    self,
                                    "End-to-End Workflow Complete",
                                    f"🎉 Workflow completed!\n\n"
                                    f"📊 Results:\n"
                                    f"• Status: {workflow_status}\n"
                                    f"• Steps completed: {steps_completed}\n"
                                    f"• Errors: {errors}\n"
                                    f"• Conversations loaded: {results.get('results', {}).get('conversations_loaded', 0)}\n\n"
                                    f"🔄 Refresh dashboard to see updated stats!",
                                )

                            # Refresh dashboard
                            self.refresh_dashboard_data()

                        except Exception as e:
                            logger.error(f"Failed to update UI after workflow: {e}")

                    # Schedule UI update on main thread
                    QTimer.singleShot(0, update_ui)

                finally:
                    loop.close()

            except Exception as e:
                logger.error(f"End-to-end workflow failed: {e}")
                
                # Schedule error display on main thread
                def show_error():
                    try:
                        self.show_error(f"End-to-end workflow failed: {e}")
                    except Exception as ui_error:
                        logger.error(f"Failed to show error dialog: {ui_error}")
                
                QTimer.singleShot(0, show_error)

        # Run in background thread
        Thread(target=_run_workflow, daemon=True).start()
        self.statusBar().showMessage("🚀 Starting end-to-end workflow...", 3000)

    # EDIT START: Handle template_applied signal for global integration
    @debug_button("_on_template_applied", "Main Window")
    def _on_template_applied(self, payload: dict):
        """Handle template application."""
        try:
            template_name = payload.get("template_name", "Unknown")
            logger.info(f"Template applied: {template_name}")
            
            # Update relevant panels
            if hasattr(self, "conversations_panel"):
                self.conversations_panel.refresh_conversations()
            
            if hasattr(self, "dashboard_panel"):
                self.dashboard_panel.refresh_data()
                
        except Exception as e:
            logger.error(f"Error handling template application: {e}")

    # EDIT END

    def show_unified_export_center(self):
        """Show the Unified Export Center."""
        if hasattr(self, 'unified_export_center'):
            self.unified_export_center.show()
        else:
            # Initialize if not already done
            self.unified_export_center = UnifiedExportCenter()
            self.unified_export_center.show()

    def show_data_loader(self):
        """Show the Unified Data Loading System."""
        if hasattr(self, 'unified_data_loader'):
            self.unified_data_loader.show_loader()
        else:
            QMessageBox.warning(self, "Data Loader", "Unified Data Loading System not initialized.")
    
    def on_data_load_completed(self, operation_id: str, success: bool, message: str, result: Any):
        """Handle data load completion."""
        if success:
            # Update status bar
            self.statusBar().showMessage(f"Data load completed: {message}", 5000)
        else:
            # Show error message
            QMessageBox.warning(self, "Load Error", f"Data load failed: {message}")
    
    def on_cache_updated(self, cache_key: str, data: Any):
        """Handle cache updates."""
        # Update status bar
        self.statusBar().showMessage(f"Cache updated: {cache_key}", 3000)


def main():
    """Main function to run the application."""
    app = QApplication(sys.argv)
    app.setApplicationName("Thea - Dreamscape MMORPG Platform")
    app.setApplicationVersion("1.0.0")
    
    # Apply global dark theme
    app.setStyleSheet("""
        QWidget {
            background-color: #2b2b2b;
            color: #ffffff;
        }
        QMainWindow {
            background-color: #1a1a1a;
            color: #ffffff;
        }
        QDialog {
            background-color: #2b2b2b;
            color: #ffffff;
        }
        QMessageBox {
            background-color: #2b2b2b;
            color: #ffffff;
        }
        QMessageBox QLabel {
            color: #ffffff;
        }
        QMessageBox QPushButton {
            background-color: #404040;
            border: 1px solid #606060;
            border-radius: 4px;
            padding: 8px 16px;
            color: #ffffff;
            min-width: 60px;
        }
        QMessageBox QPushButton:hover {
            background-color: #505050;
            border-color: #64b5f6;
        }
        QMessageBox QPushButton:pressed {
            background-color: #353535;
        }
        QTabWidget::pane {
            border: 1px solid #404040;
            background-color: #2b2b2b;
        }
        QTabWidget::tab-bar {
            left: 5px;
        }
        QTabBar::tab {
            background-color: #404040;
            color: #ffffff;
            border: 1px solid #606060;
            padding: 8px 16px;
            margin-right: 2px;
        }
        QTabBar::tab:selected {
            background-color: #64b5f6;
            color: #ffffff;
        }
        QTabBar::tab:hover {
            background-color: #505050;
        }
        QGroupBox {
            color: #ffffff;
            border: 1px solid #404040;
            border-radius: 5px;
            margin: 10px 0px;
            padding-top: 10px;
        }
        QGroupBox::title {
            color: #ffffff;
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 5px 0 5px;
        }
        QPushButton {
            background-color: #404040;
            border: 1px solid #606060;
            border-radius: 4px;
            padding: 8px 16px;
            color: #ffffff;
        }
        QPushButton:hover {
            background-color: #505050;
            border-color: #64b5f6;
        }
        QPushButton:pressed {
            background-color: #353535;
        }
        QLabel {
            color: #ffffff;
        }
        QLineEdit {
            background-color: #404040;
            border: 1px solid #606060;
            border-radius: 4px;
            padding: 4px;
            color: #ffffff;
        }
        QLineEdit:focus {
            border-color: #64b5f6;
        }
        QTextEdit {
            background-color: #404040;
            border: 1px solid #606060;
            color: #ffffff;
        }
        QListWidget {
            background-color: #404040;
            border: 1px solid #606060;
            color: #ffffff;
        }
        QTreeWidget {
            background-color: #404040;
            border: 1px solid #606060;
            color: #ffffff;
        }
        QProgressBar {
            border: 1px solid #404040;
            border-radius: 4px;
            background-color: #1e1e1e;
            text-align: center;
            color: #ffffff;
        }
        QProgressBar::chunk {
            background-color: #4caf50;
            border-radius: 3px;
        }
        QMenuBar {
            background-color: #2b2b2b;
            color: #ffffff;
        }
        QMenuBar::item:selected {
            background-color: #404040;
        }
        QMenu {
            background-color: #2b2b2b;
            color: #ffffff;
            border: 1px solid #404040;
        }
        QMenu::item:selected {
            background-color: #404040;
        }
        QStatusBar {
            background-color: #1e1e1e;
            color: #ffffff;
            border-top: 1px solid #404040;
        }
        QScrollBar:vertical {
            background-color: #404040;
            width: 15px;
            border-radius: 7px;
        }
        QScrollBar::handle:vertical {
            background-color: #606060;
            border-radius: 7px;
            min-height: 20px;
        }
        QScrollBar::handle:vertical:hover {
            background-color: #64b5f6;
        }
        QScrollBar:horizontal {
            background-color: #404040;
            height: 15px;
            border-radius: 7px;
        }
        QScrollBar::handle:horizontal {
            background-color: #606060;
            border-radius: 7px;
            min-width: 20px;
        }
        QScrollBar::handle:horizontal:hover {
            background-color: #64b5f6;
        }
    """)

    window = TheaMainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
