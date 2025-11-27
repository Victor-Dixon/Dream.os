#!/usr/bin/env python3
"""
Unified Conversation Workflow
============================

Unified conversation workflow for processing conversations with full integration.
"""

import logging
from datetime import datetime
from typing import Dict, List, Any

from ..models.processing_result import ProcessingResult
from ..config.workflow_config import WorkflowConfig
from ..processors.template_processor import TemplateProcessor
from ..processors.discord_processor import DiscordProcessor
from ..processors.game_processor import GameProcessor
from ..processors.content_processor import ContentProcessor

logger = logging.getLogger(__name__)


class UnifiedConversationWorkflow:
    """Unified conversation workflow for processing conversations."""
    
    def __init__(self, memory_manager=None, template_engine=None,
                 discord_manager=None, mmorpg_engine=None, config: WorkflowConfig = None):
        """
        Initialize the unified conversation workflow.
        
        Args:
            memory_manager: Memory manager instance
            template_engine: Template engine instance
            discord_manager: Discord manager instance
            mmorpg_engine: MMORPG engine instance
            config: Workflow configuration
        """
        self.memory_manager = memory_manager
        self.template_engine = template_engine
        self.discord_manager = discord_manager
        self.mmorpg_engine = mmorpg_engine
        self.config = config or WorkflowConfig()
        self.processed_conversations = set()
        
        # Initialize processors
        self.template_processor = TemplateProcessor(template_engine)
        self.discord_processor = DiscordProcessor(discord_manager)
        self.game_processor = GameProcessor(mmorpg_engine)
        self.content_processor = ContentProcessor()
    
    def process_conversations_batch(self, conversations: List[Dict]) -> List[ProcessingResult]:
        """Process conversations in batch mode with improved error handling."""
        logger.info(f"Processing {len(conversations)} conversations in batch mode")
        results = []
        batch_errors = []  # EDIT: Collect errors for batch summary
        for conversation in conversations:
            try:
                result = self._process_single_conversation(conversation)
                results.append(result)
                if result.error:
                    batch_errors.append({
                        'conversation_id': result.conversation_id,
                        'error': result.error
                    })
            except KeyError as e:
                msg = f"Missing required field: {e}. Please check conversation data format."
                logger.error(f"KeyError processing conversation {conversation.get('id', 'unknown')}: {msg}")
                results.append(ProcessingResult(
                    conversation_id=conversation.get('id', 'unknown'),
                    title=conversation.get('title', 'Unknown'),
                    success=False,
                    template_applied=False,
                    discord_posted=False,
                    game_updated=False,
                    content_extracted=False,
                    error=msg,
                    timestamp=datetime.now()
                ))
                batch_errors.append({'conversation_id': conversation.get('id', 'unknown'), 'error': msg})
            except ValueError as e:
                msg = f"Value error: {e}. Please check input values."
                logger.error(f"ValueError processing conversation {conversation.get('id', 'unknown')}: {msg}")
                results.append(ProcessingResult(
                    conversation_id=conversation.get('id', 'unknown'),
                    title=conversation.get('title', 'Unknown'),
                    success=False,
                    template_applied=False,
                    discord_posted=False,
                    game_updated=False,
                    content_extracted=False,
                    error=msg,
                    timestamp=datetime.now()
                ))
                batch_errors.append({'conversation_id': conversation.get('id', 'unknown'), 'error': msg})
            except Exception as e:
                msg = f"Unexpected error: {e}. Please report this issue."
                logger.error(f"Error processing conversation {conversation.get('id', 'unknown')}: {msg}")
                results.append(ProcessingResult(
                    conversation_id=conversation.get('id', 'unknown'),
                    title=conversation.get('title', 'Unknown'),
                    success=False,
                    template_applied=False,
                    discord_posted=False,
                    game_updated=False,
                    content_extracted=False,
                    error=msg,
                    timestamp=datetime.now()
                ))
                batch_errors.append({'conversation_id': conversation.get('id', 'unknown'), 'error': msg})
        # EDIT: Log batch summary if any errors
        if batch_errors:
            logger.warning(f"Batch processing completed with {len(batch_errors)} errors. See error summary below:")
            for err in batch_errors:
                logger.warning(f"  Conversation {err['conversation_id']}: {err['error']}")
        return results
    
    def process_conversations_incremental(self, conversations: List[Dict]) -> List[ProcessingResult]:
        """Process conversations incrementally (only new ones)."""
        logger.info(f"Processing {len(conversations)} conversations incrementally")
        results = []
        
        for conversation in conversations:
            if not self._is_already_processed(conversation):
                try:
                    result = self._process_single_conversation(conversation)
                    results.append(result)
                    self._mark_as_processed(conversation)
                except Exception as e:
                    logger.error(f"Error processing conversation {conversation.get('id', 'unknown')}: {e}")
                    results.append(ProcessingResult(
                        conversation_id=conversation.get('id', 'unknown'),
                        title=conversation.get('title', 'Unknown'),
                        success=False,
                        template_applied=False,
                        discord_posted=False,
                        game_updated=False,
                        content_extracted=False,
                        error=str(e),
                        timestamp=datetime.now()
                    ))
            else:
                logger.debug(f"Conversation {conversation.get('id', 'unknown')} already processed, skipping")
        
        return results
    
    def _is_already_processed(self, conversation: Dict) -> bool:
        """Check if conversation has already been processed."""
        conv_id = conversation.get('id', 'unknown')
        return conv_id in self.processed_conversations
    
    def _mark_as_processed(self, conversation: Dict):
        """Mark conversation as processed."""
        conv_id = conversation.get('id', 'unknown')
        self.processed_conversations.add(conv_id)
    
    def _process_single_conversation(self, conversation: Dict) -> ProcessingResult:
        """Process a single conversation with improved error handling."""
        start_time = datetime.now()
        conv_id = conversation.get('id', 'unknown')
        try:
            # Apply templates
            template_applied = self._apply_templates(conversation)
            # Extract content
            content_extracted = self._extract_content(conversation)
            # Update game state
            game_updated = self._update_game_state(conversation)
            # Post to Discord
            discord_posted = self._post_to_discord(conversation)
            # Calculate processing time
            processing_time = (datetime.now() - start_time).total_seconds()
            return ProcessingResult(
                conversation_id=conv_id,
                title=conversation.get('title', 'Untitled'),
                success=True,
                template_applied=template_applied,
                discord_posted=discord_posted,
                game_updated=game_updated,
                content_extracted=content_extracted,
                processing_time=processing_time,
                timestamp=datetime.now()
            )
        except KeyError as e:
            msg = f"Missing required field: {e}. Please check conversation data format."
            logger.error(f"KeyError processing conversation {conv_id}: {msg}")
            return ProcessingResult(
                conversation_id=conv_id,
                title=conversation.get('title', 'Unknown'),
                success=False,
                template_applied=False,
                discord_posted=False,
                game_updated=False,
                content_extracted=False,
                error=msg,
                processing_time=(datetime.now() - start_time).total_seconds(),
                timestamp=datetime.now()
            )
        except ValueError as e:
            msg = f"Value error: {e}. Please check input values."
            logger.error(f"ValueError processing conversation {conv_id}: {msg}")
            return ProcessingResult(
                conversation_id=conv_id,
                title=conversation.get('title', 'Unknown'),
                success=False,
                template_applied=False,
                discord_posted=False,
                game_updated=False,
                content_extracted=False,
                error=msg,
                processing_time=(datetime.now() - start_time).total_seconds(),
                timestamp=datetime.now()
            )
        except Exception as e:
            msg = f"Unexpected error: {e}. Please report this issue."
            logger.error(f"Error processing conversation {conv_id}: {msg}")
            return ProcessingResult(
                conversation_id=conv_id,
                title=conversation.get('title', 'Unknown'),
                success=False,
                template_applied=False,
                discord_posted=False,
                game_updated=False,
                content_extracted=False,
                error=msg,
                processing_time=(datetime.now() - start_time).total_seconds(),
                timestamp=datetime.now()
            )
    
    def _apply_templates(self, conversation: Dict) -> bool:
        """Apply templates to conversation."""
        if not self.config.enable_templates:
            return False
        
        try:
            return self.template_processor.apply_templates(conversation)
        except Exception as e:
            logger.error(f"Error applying templates: {e}")
            return False
    
    def _post_to_discord(self, conversation: Dict) -> bool:
        """Post conversation to Discord."""
        if not self.config.enable_discord:
            return False
        
        try:
            return self.discord_processor.post_to_discord(conversation)
        except Exception as e:
            logger.error(f"Error posting to Discord: {e}")
            return False
    
    def _update_game_state(self, conversation: Dict) -> bool:
        """Update game state based on conversation."""
        if not self.config.enable_game_updates:
            return False
        
        try:
            return self.game_processor.update_game_state(conversation)
        except Exception as e:
            logger.error(f"Error updating game state: {e}")
            return False
    
    def _extract_content(self, conversation: Dict) -> bool:
        """Extract content from conversation."""
        if not self.config.enable_content_extraction:
            return False
        
        try:
            return self.content_processor.extract_content(conversation)
        except Exception as e:
            logger.error(f"Error extracting content: {e}")
            return False
    
    def get_processing_stats(self) -> Dict[str, Any]:
        """Get processing statistics."""
        return {
            'total_processed': len(self.processed_conversations),
            'template_stats': self.template_processor.get_applied_templates(),
            'discord_stats': self.discord_processor.get_discord_stats(),
            'game_stats': self.game_processor.get_game_stats(),
            'content_stats': self.content_processor.get_content_stats()
        }
    
    def clear_processing_data(self):
        """Clear all processing data."""
        self.processed_conversations.clear()
        self.template_processor.clear_applied_templates()
        self.discord_processor.clear_posted_messages()
        self.game_processor.clear_game_updates()
        self.content_processor.clear_extracted_content() 