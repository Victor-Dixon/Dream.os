#!/usr/bin/env python3
"""
Memory Data Extractor
====================

Extracts various data types from conversation corpus for weaponization.
"""

import logging
from typing import Dict, List, Optional, Any

logger = logging.getLogger(__name__)


class DataExtractor:
    """Extracts various data types from conversation corpus."""
    
    def __init__(self):
        """Initialize the data extractor."""
        pass
    
    def extract_conversation_pairs(self, conversations: List[Dict]) -> List[Dict]:
        """
        Extract conversation pairs for training.
        
        Args:
            conversations: List of conversation dictionaries
            
        Returns:
            List of conversation pairs
        """
        pairs = []
        
        for conv in conversations:
            messages = conv.get('messages', [])
            if len(messages) >= 2:
                # Extract user-assistant pairs
                for i in range(len(messages) - 1):
                    if (messages[i].get('role') == 'user' and 
                        messages[i + 1].get('role') == 'assistant'):
                        pairs.append({
                            'conversation_id': conv.get('id'),
                            'user_message': messages[i].get('content', ''),
                            'assistant_message': messages[i + 1].get('content', ''),
                            'timestamp': conv.get('timestamp', '')
                        })
        
        logger.info(f"Extracted {len(pairs)} conversation pairs")
        return pairs
    
    def extract_qa_pairs(self, conversations: List[Dict]) -> List[Dict]:
        """
        Extract question-answer pairs from conversations.
        
        Args:
            conversations: List of conversation dictionaries
            
        Returns:
            List of QA pairs
        """
        qa_pairs = []
        
        for conv in conversations:
            messages = conv.get('messages', [])
            if len(messages) >= 2:
                for i in range(len(messages) - 1):
                    user_msg = messages[i].get('content', '')
                    assistant_msg = messages[i + 1].get('content', '')
                    
                    # Check if this looks like a Q&A pair
                    if (messages[i].get('role') == 'user' and 
                        messages[i + 1].get('role') == 'assistant' and
                        self._is_question(user_msg) and
                        self._is_answer(assistant_msg)):
                        
                        qa_pairs.append({
                            'conversation_id': conv.get('id'),
                            'question': user_msg,
                            'answer': assistant_msg,
                            'category': self._categorize_qa(user_msg),
                            'timestamp': conv.get('timestamp', '')
                        })
        
        logger.info(f"Extracted {len(qa_pairs)} QA pairs")
        return qa_pairs
    
    def extract_instructions(self, conversations: List[Dict]) -> List[Dict]:
        """
        Extract instruction-following examples from conversations.
        
        Args:
            conversations: List of conversation dictionaries
            
        Returns:
            List of instruction examples
        """
        instructions = []
        
        for conv in conversations:
            messages = conv.get('messages', [])
            if len(messages) >= 2:
                for i in range(len(messages) - 1):
                    user_msg = messages[i].get('content', '')
                    assistant_msg = messages[i + 1].get('content', '')
                    
                    if (messages[i].get('role') == 'user' and 
                        messages[i + 1].get('role') == 'assistant' and
                        self._is_instruction(user_msg)):
                        
                        instructions.append({
                            'conversation_id': conv.get('id'),
                            'instruction': user_msg,
                            'execution': assistant_msg,
                            'success': self._assess_instruction_success(user_msg, assistant_msg),
                            'timestamp': conv.get('timestamp', '')
                        })
        
        logger.info(f"Extracted {len(instructions)} instruction examples")
        return instructions
    
    def extract_code_examples(self, conversations: List[Dict]) -> List[Dict]:
        """
        Extract code examples from conversations.
        
        Args:
            conversations: List of conversation dictionaries
            
        Returns:
            List of code examples
        """
        code_examples = []
        
        for conv in conversations:
            messages = conv.get('messages', [])
            for msg in messages:
                content = msg.get('content', '')
                if self._contains_code(content):
                    code_examples.append({
                        'conversation_id': conv.get('id'),
                        'role': msg.get('role'),
                        'code': self._extract_code_blocks(content),
                        'language': self._detect_language(content),
                        'timestamp': conv.get('timestamp', '')
                    })
        
        logger.info(f"Extracted {len(code_examples)} code examples")
        return code_examples
    
    def is_problem_solving_conversation(self, conv: Dict) -> bool:
        """
        Check if a conversation is about problem-solving.
        
        Args:
            conv: Conversation dictionary
            
        Returns:
            True if problem-solving conversation
        """
        content = ' '.join([msg.get('content', '') for msg in conv.get('messages', [])])
        content_lower = content.lower()
        
        problem_keywords = [
            'error', 'bug', 'fix', 'issue', 'problem', 'troubleshoot',
            'debug', 'solve', 'resolve', 'help', 'how to', 'why',
            'broken', 'not working', 'failed', 'exception'
        ]
        
        return any(keyword in content_lower for keyword in problem_keywords)
    
    def _is_question(self, text: str) -> bool:
        """Check if text contains a question."""
        question_indicators = ['?', 'how', 'what', 'why', 'when', 'where', 'who', 'which']
        text_lower = text.lower()
        return any(indicator in text_lower for indicator in question_indicators)
    
    def _is_answer(self, text: str) -> bool:
        """Check if text looks like an answer."""
        # Simple heuristic: longer than 50 chars and contains explanation
        return len(text) > 50 and any(word in text.lower() for word in ['because', 'since', 'therefore', 'thus'])
    
    def _is_instruction(self, text: str) -> bool:
        """Check if text contains an instruction."""
        instruction_indicators = [
            'create', 'build', 'make', 'write', 'implement', 'add', 'remove',
            'update', 'modify', 'change', 'fix', 'install', 'configure'
        ]
        text_lower = text.lower()
        return any(indicator in text_lower for indicator in instruction_indicators)
    
    def _categorize_qa(self, question: str) -> str:
        """Categorize a question."""
        question_lower = question.lower()
        
        if any(word in question_lower for word in ['error', 'bug', 'fix', 'problem']):
            return 'troubleshooting'
        elif any(word in question_lower for word in ['how', 'create', 'build', 'make']):
            return 'how-to'
        elif any(word in question_lower for word in ['what', 'why', 'explain']):
            return 'explanation'
        else:
            return 'general'
    
    def _assess_instruction_success(self, instruction: str, execution: str) -> bool:
        """Assess if instruction execution was successful."""
        # Simple heuristic: execution should be substantial
        return len(execution) > len(instruction) * 0.5
    
    def _contains_code(self, text: str) -> bool:
        """Check if text contains code blocks."""
        return '```' in text or any(keyword in text.lower() for keyword in ['def ', 'class ', 'import ', 'function', 'var ', 'const '])
    
    def _extract_code_blocks(self, text: str) -> List[str]:
        """Extract code blocks from text."""
        import re
        code_blocks = re.findall(r'```(?:\w+)?\n(.*?)\n```', text, re.DOTALL)
        return [block.strip() for block in code_blocks]
    
    def _detect_language(self, text: str) -> str:
        """Detect programming language from text."""
        text_lower = text.lower()
        
        if 'def ' in text_lower or 'import ' in text_lower:
            return 'python'
        elif 'function ' in text_lower or 'var ' in text_lower:
            return 'javascript'
        elif 'class ' in text_lower and 'public ' in text_lower:
            return 'java'
        elif '#' in text_lower and 'include' in text_lower:
            return 'c'
        else:
            return 'unknown' 