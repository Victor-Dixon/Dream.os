#!/usr/bin/env python3
"""
Daily Conversation Pipeline
==========================

Daily processing pipeline for handling routine conversation processing.
"""

import logging
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any
from pathlib import Path

from ..models.processing_result import ProcessingResult
from ..config.workflow_config import WorkflowConfig
from ..processors.template_processor import TemplateProcessor
from ..processors.discord_processor import DiscordProcessor
from ..processors.game_processor import GameProcessor
from ..processors.content_processor import ContentProcessor

logger = logging.getLogger(__name__)


class DailyConversationPipeline:
    """Daily conversation processing pipeline."""
    
    def __init__(self, memory_manager=None, config: WorkflowConfig = None):
        """
        Initialize the daily conversation pipeline.
        
        Args:
            memory_manager: Memory manager instance
            config: Workflow configuration
        """
        self.memory_manager = memory_manager
        self.config = config or WorkflowConfig()
        
        # Initialize processors
        self.template_processor = TemplateProcessor()
        self.discord_processor = DiscordProcessor()
        self.game_processor = GameProcessor()
        self.content_processor = ContentProcessor()
        
        # Setup output directory
        self.output_dir = Path(self.config.output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def run_daily_processing(self) -> List[ProcessingResult]:
        """Run daily processing pipeline with improved error handling."""
        logger.info("Starting daily conversation processing")
        try:
            # Get recent conversations (last 24 hours)
            since = datetime.now() - timedelta(days=1)
            conversations = self._get_recent_conversations(since)
            if not conversations:
                logger.info("No recent conversations found for daily processing")
                return []
            logger.info(f"Found {len(conversations)} conversations for daily processing")
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
            # Generate daily report
            self._generate_daily_report(results)
            logger.info(f"Daily processing completed. Processed {len(results)} conversations")
            return results
        except Exception as e:
            logger.error(f"Error in daily processing: {e}")
            return []
    
    def _get_recent_conversations(self, since: datetime) -> List[Dict]:
        """Get recent conversations since the specified time."""
        try:
            if self.memory_manager:
                # Get conversations from memory manager
                all_conversations = self.memory_manager.get_recent_conversations(100)
                
                # Filter by timestamp
                recent_conversations = []
                for conv in all_conversations:
                    conv_timestamp = conv.get('timestamp')
                    if conv_timestamp:
                        try:
                            conv_datetime = datetime.fromisoformat(conv_timestamp.replace('Z', '+00:00'))
                            if conv_datetime >= since:
                                recent_conversations.append(conv)
                        except ValueError:
                            # Skip conversations with invalid timestamps
                            continue
                
                return recent_conversations
            else:
                logger.warning("Memory manager not available, returning empty list")
                return []
                
        except Exception as e:
            logger.error(f"Error getting recent conversations: {e}")
            return []
    
    def _process_single_conversation(self, conversation: Dict) -> ProcessingResult:
        """Process a single conversation for daily processing with improved error handling."""
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
    
    def _extract_content(self, conversation: Dict) -> bool:
        """Extract content from conversation."""
        if not self.config.enable_content_extraction:
            return False
        
        try:
            return self.content_processor.extract_content(conversation)
        except Exception as e:
            logger.error(f"Error extracting content: {e}")
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
    
    def _post_to_discord(self, conversation: Dict) -> bool:
        """Post conversation to Discord."""
        if not self.config.enable_discord:
            return False
        
        try:
            return self.discord_processor.post_to_discord(conversation)
        except Exception as e:
            logger.error(f"Error posting to Discord: {e}")
            return False
    
    def _generate_daily_report(self, results: List[ProcessingResult]):
        """Generate daily processing report."""
        try:
            # Calculate statistics
            total_processed = len(results)
            successful = len([r for r in results if r.success])
            failed = total_processed - successful
            
            template_applied = len([r for r in results if r.template_applied])
            discord_posted = len([r for r in results if r.discord_posted])
            game_updated = len([r for r in results if r.game_updated])
            content_extracted = len([r for r in results if r.content_extracted])
            
            total_processing_time = sum(r.processing_time for r in results)
            avg_processing_time = total_processing_time / total_processed if total_processed > 0 else 0
            
            # Create report
            report = {
                'date': datetime.now().isoformat(),
                'summary': {
                    'total_processed': total_processed,
                    'successful': successful,
                    'failed': failed,
                    'success_rate': (successful / total_processed * 100) if total_processed > 0 else 0
                },
                'operations': {
                    'template_applied': template_applied,
                    'discord_posted': discord_posted,
                    'game_updated': game_updated,
                    'content_extracted': content_extracted
                },
                'performance': {
                    'total_processing_time': total_processing_time,
                    'avg_processing_time': avg_processing_time
                },
                'errors': [
                    {
                        'conversation_id': r.conversation_id,
                        'error': r.error
                    }
                    for r in results if r.error
                ]
            }
            
            # Save report
            report_filename = f"daily_report_{datetime.now().strftime('%Y%m%d')}.json"
            report_path = self.output_dir / report_filename
            
            with open(report_path, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Daily report saved to: {report_path}")
            
        except Exception as e:
            logger.error(f"Error generating daily report: {e}")
    
    def get_processing_stats(self) -> Dict[str, Any]:
        """Get processing statistics."""
        return {
            'template_stats': self.template_processor.get_applied_templates(),
            'discord_stats': self.discord_processor.get_discord_stats(),
            'game_stats': self.game_processor.get_game_stats(),
            'content_stats': self.content_processor.get_content_stats(),
            'output_directory': str(self.output_dir)
        }
    
    def clear_processing_data(self):
        """Clear all processing data."""
        self.template_processor.clear_applied_templates()
        self.discord_processor.clear_posted_messages()
        self.game_processor.clear_game_updates()
        self.content_processor.clear_extracted_content() 