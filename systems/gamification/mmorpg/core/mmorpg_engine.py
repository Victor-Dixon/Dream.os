#!/usr/bin/env python3
"""
MMORPG Core Engine
==================

Core engine for the Dreamscape MMORPG system.
Handles game state management, player progression, and core game mechanics.
"""

import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
from pathlib import Path
import json
import sqlite3

from ..models.mmorpg_models import (
    Player, GameState, Quest, Skill, ArchitectTier, Guild,
    QuestType, SkillType, MMORPGConfig
)

logger = logging.getLogger(__name__)


class MMORPGEngine:
    """Core MMORPG engine for managing game state and progression."""
    
    def __init__(self, db_path: str = "dreamos_resume.db", config: MMORPGConfig = None):
        """Initialize the MMORPG engine."""
        self.db_path = db_path
        self.config = config or MMORPGConfig()
        self.connection = None
        self.player = None
        self.game_state = None
        
        # Initialize database and load game state
        self._initialize_database()
        self._load_game_state()
        
        logger.info("MMORPG Engine initialized")
    
    def _initialize_database(self):
        """Initialize the MMORPG database."""
        try:
            self.connection = sqlite3.connect(self.db_path)
            self.connection.row_factory = sqlite3.Row
            
            # Create tables if they don't exist
            self._create_tables()
            
        except Exception as e:
            logger.error(f"Failed to initialize MMORPG database: {e}")
            raise
    
    def _create_tables(self):
        """Create MMORPG database tables."""
        cursor = self.connection.cursor()
        
        # Players table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS players (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                architect_tier TEXT DEFAULT 'Tier 1 - Novice',
                xp INTEGER DEFAULT 0,
                total_conversations INTEGER DEFAULT 0,
                total_messages INTEGER DEFAULT 0,
                total_words INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Skills table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS skills (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                player_id INTEGER,
                name TEXT NOT NULL,
                current_level INTEGER DEFAULT 0,
                experience_points INTEGER DEFAULT 0,
                max_level INTEGER DEFAULT 100,
                last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (player_id) REFERENCES players (id)
            )
        """)
        
        # Quests table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS quests (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                player_id INTEGER,
                title TEXT NOT NULL,
                description TEXT,
                quest_type TEXT NOT NULL,
                difficulty INTEGER DEFAULT 1,
                xp_reward INTEGER DEFAULT 0,
                skill_rewards TEXT,  -- JSON string
                status TEXT DEFAULT 'available',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                completed_at TIMESTAMP,
                conversation_id TEXT,
                FOREIGN KEY (player_id) REFERENCES players (id)
            )
        """)
        
        # Architect tiers table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS architect_tiers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                player_id INTEGER,
                tier_level INTEGER NOT NULL,
                tier_name TEXT NOT NULL,
                experience_required INTEGER NOT NULL,
                abilities_unlocked TEXT,  -- JSON string
                achieved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (player_id) REFERENCES players (id)
            )
        """)
        
        # Guilds table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS guilds (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                leader_id INTEGER,
                members TEXT,  -- JSON string
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (leader_id) REFERENCES players (id)
            )
        """)
        
        self.connection.commit()
        logger.info("MMORPG database tables created/verified")
    
    def _load_game_state(self):
        """Load the current game state from database."""
        try:
            # Load or create player
            self.player = self._load_or_create_player()
            
            # Load game state
            self.game_state = self._load_game_state_from_db()
            
            logger.info(f"Game state loaded for player: {self.player.name}")
            
        except Exception as e:
            logger.error(f"Failed to load game state: {e}")
            raise
    
    def _load_or_create_player(self) -> Player:
        """Load existing player or create a new one."""
        cursor = self.connection.cursor()
        
        # Try to load existing player
        cursor.execute("SELECT * FROM players ORDER BY id DESC LIMIT 1")
        row = cursor.fetchone()
        
        if row:
            # Load existing player
            player = Player(
                name=row['name'],
                architect_tier=row['architect_tier'],
                xp=row['xp'],
                total_conversations=row['total_conversations'],
                total_messages=row['total_messages'],
                total_words=row['total_words'],
                created_at=datetime.fromisoformat(row['created_at']),
                last_active=datetime.fromisoformat(row['last_active'])
            )
        else:
            # Create new player
            player = Player(
                name="Dreamscape Architect",
                architect_tier="Tier 1 - Novice",
                xp=0,
                total_conversations=0,
                total_messages=0,
                total_words=0,
                created_at=datetime.now(),
                last_active=datetime.now()
            )
            
            # Save new player to database
            cursor.execute("""
                INSERT INTO players (name, architect_tier, xp, total_conversations, 
                                   total_messages, total_words, created_at, last_active)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                player.name, player.architect_tier, player.xp,
                player.total_conversations, player.total_messages, player.total_words,
                player.created_at.isoformat(), player.last_active.isoformat()
            ))
            self.connection.commit()
            
            logger.info("New player created")
        
        return player
    
    def _load_game_state_from_db(self) -> GameState:
        """Load game state from database."""
        cursor = self.connection.cursor()
        
        # Load skills
        cursor.execute("SELECT * FROM skills WHERE player_id = 1")
        skill_rows = cursor.fetchall()
        skills = {}
        
        for row in skill_rows:
            skill = Skill(
                name=row['name'],
                current_level=row['current_level'],
                experience_points=row['experience_points'],
                max_level=row['max_level'],
                last_updated=datetime.fromisoformat(row['last_updated'])
            )
            skills[skill.name] = skill
        
        # Load quests
        cursor.execute("SELECT * FROM quests WHERE player_id = 1")
        quest_rows = cursor.fetchall()
        quests = {}
        
        for row in quest_rows:
            skill_rewards = json.loads(row['skill_rewards']) if row['skill_rewards'] else {}
            quest = Quest(
                id=str(row['id']),
                title=row['title'],
                description=row['description'],
                quest_type=QuestType(row['quest_type']),
                difficulty=row['difficulty'],
                xp_reward=row['xp_reward'],
                skill_rewards=skill_rewards,
                status=row['status'],
                created_at=datetime.fromisoformat(row['created_at']) if row['created_at'] else None,
                completed_at=datetime.fromisoformat(row['completed_at']) if row['completed_at'] else None,
                conversation_id=row['conversation_id']
            )
            quests[quest.id] = quest
        
        # Load architect tiers
        cursor.execute("SELECT * FROM architect_tiers WHERE player_id = 1")
        tier_rows = cursor.fetchall()
        architect_tiers = {}
        
        for row in tier_rows:
            abilities_unlocked = json.loads(row['abilities_unlocked']) if row['abilities_unlocked'] else []
            tier = ArchitectTier(
                tier_level=row['tier_level'],
                tier_name=row['tier_name'],
                experience_required=row['experience_required'],
                abilities_unlocked=abilities_unlocked,
                achieved_at=datetime.fromisoformat(row['achieved_at']) if row['achieved_at'] else None
            )
            architect_tiers[tier.tier_level] = tier
        
        # Load guilds
        cursor.execute("SELECT * FROM guilds")
        guild_rows = cursor.fetchall()
        guilds = {}
        
        for row in guild_rows:
            members = json.loads(row['members']) if row['members'] else []
            guild = Guild(
                id=str(row['id']),
                name=row['name'],
                description=row['description'],
                leader_id=str(row['leader_id']) if row['leader_id'] else "",
                members=members,
                created_at=datetime.fromisoformat(row['created_at']) if row['created_at'] else None
            )
            guilds[guild.id] = guild
        
        # Create game state
        game_state = GameState(
            current_tier=self._get_current_tier(),
            total_xp=self.player.xp,
            skills=skills,
            quests=quests,
            architect_tiers=architect_tiers,
            guilds=guilds,
            last_updated=datetime.now()
        )
        
        return game_state
    
    def _get_current_tier(self) -> int:
        """Get the current architect tier level."""
        try:
            tier_parts = self.player.architect_tier.split()
            if len(tier_parts) >= 2:
                return int(tier_parts[1])
            return 1
        except (ValueError, IndexError):
            return 1
    
    def get_player_info(self) -> Dict[str, Any]:
        """Get current player information."""
        return {
            "name": self.player.name,
            "architect_tier": self.player.architect_tier,
            "xp": self.player.xp,
            "next_level_xp": self.player.get_next_level_xp(),
            "total_conversations": self.player.total_conversations,
            "total_messages": self.player.total_messages,
            "total_words": self.player.total_words,
            "created_at": self.player.created_at.isoformat(),
            "last_active": self.player.last_active.isoformat()
        }
    
    def get_player(self) -> Player:
        """Get the current player object."""
        return self.player
    
    def get_active_quests(self) -> List[Quest]:
        """Get all active quests."""
        return [quest for quest in self.game_state.quests.values() if quest.status == "active"]
    
    def get_available_quests(self) -> List[Quest]:
        """Get all available quests."""
        return [quest for quest in self.game_state.quests.values() if quest.status == "available"]
    
    def get_skills(self) -> Dict[str, Skill]:
        """Get all player skills."""
        return self.game_state.skills
    
    def get_skill(self, skill_name: str) -> Optional[Skill]:
        """Get a specific skill by name."""
        return self.game_state.skills.get(skill_name)
    
    def award_xp(self, amount: int, skill_rewards: Dict[str, int] = None):
        """Award XP to the player."""
        self.player.xp += amount
        self.player.last_active = datetime.now()
        
        # Update skills if provided
        if skill_rewards:
            for skill_name, xp_amount in skill_rewards.items():
                if skill_name in self.game_state.skills:
                    self.game_state.skills[skill_name].experience_points += xp_amount
                    self.game_state.skills[skill_name].last_updated = datetime.now()
        
        # Check for tier progression
        self._check_tier_progression()
        
        # Save to database
        self._save_player_state()
        
        logger.info(f"Awarded {amount} XP to player")
    
    def _check_tier_progression(self):
        """Check if player should progress to next tier."""
        current_tier = self._get_current_tier()
        next_tier_xp = self._get_tier_xp_requirement(current_tier + 1)
        
        if self.player.xp >= next_tier_xp:
            self._progress_to_tier(current_tier + 1)
    
    def _get_tier_xp_requirement(self, tier: int) -> int:
        """Get XP requirement for a specific tier."""
        # Simple tier progression: 1000 XP per tier
        return tier * 1000
    
    def _progress_to_tier(self, new_tier: int):
        """Progress player to a new tier."""
        tier_names = {
            1: "Tier 1 - Novice",
            2: "Tier 2 - Apprentice",
            3: "Tier 3 - Journeyman",
            4: "Tier 4 - Expert",
            5: "Tier 5 - Master",
            6: "Tier 6 - Grandmaster",
            7: "Tier 7 - Legend",
            8: "Tier 8 - Mythic",
            9: "Tier 9 - Divine",
            10: "Tier 10 - Transcendent"
        }
        
        if new_tier in tier_names:
            self.player.architect_tier = tier_names[new_tier]
            self.game_state.current_tier = new_tier
            
            # Create architect tier record
            tier = ArchitectTier(
                tier_level=new_tier,
                tier_name=tier_names[new_tier],
                experience_required=self._get_tier_xp_requirement(new_tier),
                abilities_unlocked=[],  # TODO: Define tier abilities
                achieved_at=datetime.now()
            )
            self.game_state.architect_tiers[new_tier] = tier
            
            logger.info(f"Player progressed to {tier_names[new_tier]}")
    
    def _save_player_state(self):
        """Save player state to database."""
        try:
            cursor = self.connection.cursor()
            
            # Update player
            cursor.execute("""
                UPDATE players 
                SET architect_tier = ?, xp = ?, total_conversations = ?, 
                    total_messages = ?, total_words = ?, last_active = ?
                WHERE id = 1
            """, (
                self.player.architect_tier, self.player.xp,
                self.player.total_conversations, self.player.total_messages,
                self.player.total_words, self.player.last_active.isoformat()
            ))
            
            # Update skills
            for skill in self.game_state.skills.values():
                cursor.execute("""
                    INSERT OR REPLACE INTO skills 
                    (player_id, name, current_level, experience_points, max_level, last_updated)
                    VALUES (1, ?, ?, ?, ?, ?)
                """, (
                    skill.name, skill.current_level, skill.experience_points,
                    skill.max_level, skill.last_updated.isoformat()
                ))
            
            self.connection.commit()
            
        except Exception as e:
            logger.error(f"Failed to save player state: {e}")
            raise
    
    def create_quest(self, title: str, description: str, quest_type: QuestType,
                    difficulty: int, xp_reward: int, skill_rewards: Dict[str, int] = None) -> str:
        """Create a new quest."""
        quest_id = str(len(self.game_state.quests) + 1)
        
        quest = Quest(
            id=quest_id,
            title=title,
            description=description,
            quest_type=quest_type,
            difficulty=difficulty,
            xp_reward=xp_reward,
            skill_rewards=skill_rewards or {},
            status="available",
            created_at=datetime.now()
        )
        
        self.game_state.quests[quest_id] = quest
        
        # Save to database
        cursor = self.connection.cursor()
        cursor.execute("""
            INSERT INTO quests (player_id, title, description, quest_type, difficulty,
                              xp_reward, skill_rewards, status, created_at)
            VALUES (1, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            quest.title, quest.description, quest.quest_type.value,
            quest.difficulty, quest.xp_reward, json.dumps(quest.skill_rewards),
            quest.status, quest.created_at.isoformat()
        ))
        self.connection.commit()
        
        logger.info(f"Created quest: {title}")
        return quest_id
    
    def start_quest(self, quest_id: str) -> bool:
        """Start a quest."""
        if quest_id in self.game_state.quests:
            quest = self.game_state.quests[quest_id]
            if quest.status == "available":
                quest.status = "active"
                
                # Update database
                cursor = self.connection.cursor()
                cursor.execute("""
                    UPDATE quests SET status = ? WHERE id = ?
                """, (quest.status, quest_id))
                self.connection.commit()
                
                logger.info(f"Started quest: {quest.title}")
                return True
        
        return False
    
    def complete_quest(self, quest_id: str) -> bool:
        """Complete a quest and award rewards."""
        if quest_id in self.game_state.quests:
            quest = self.game_state.quests[quest_id]
            if quest.status == "active":
                quest.status = "completed"
                quest.completed_at = datetime.now()
                
                # Award XP and skill rewards
                self.award_xp(quest.xp_reward, quest.skill_rewards)
                
                # Update database
                cursor = self.connection.cursor()
                cursor.execute("""
                    UPDATE quests SET status = ?, completed_at = ? WHERE id = ?
                """, (quest.status, quest.completed_at.isoformat(), quest_id))
                self.connection.commit()
                
                logger.info(f"Completed quest: {quest.title}")
                return True
        
        return False
    
    def get_game_state(self) -> GameState:
        """Get the current game state."""
        return self.game_state
    
    def close(self):
        """Close the MMORPG engine and database connection."""
        if self.connection:
            self.connection.close()
            logger.info("MMORPG Engine closed") 