"""
Prompt Orchestrator for Dream.OS

Coordinates between context management, template engine, and context injection
to provide intelligent prompt generation and management.
"""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime
import json
import uuid

# EDIT START: Fix import path for ContextManager and Context (was .context_manager, should be dreamscape.core.legacy.context_manager)
from dreamscape.core.legacy.context_manager import ContextManager, Context
# EDIT END
# EDIT START: Fix import path for ContextInjectionSystem and ContextConfig (was .context_injection, should be dreamscape.core.context_injection)
from dreamscape.core.context_injection import ContextInjectionSystem, ContextConfig
# EDIT END
from .template_engine import PromptTemplateEngine, PromptTemplate



@dataclass
class PromptRequest:
    goal: str
    context_type: Optional[str] = None
    template_type: Optional[str] = None
    variables: Dict = None
    metadata: Dict = None
    model_name: str = "gpt-4"
    required_context_ids: List[str] = None

@dataclass
class PromptResponse:
    prompt: str
    template_id: str
    context_ids: List[str]
    metadata: Dict
    token_usage: Dict
    created_at: datetime = None

class PromptOrchestrator:
    def __init__(self, db_path: str):
        """Initialize the orchestrator with its components."""
        self.context_manager = ContextManager(db_path)
        self.template_engine = PromptTemplateEngine(db_path)
        self.context_injection = ContextInjectionSystem(self.context_manager)

    def generate_prompt(self, request: PromptRequest) -> PromptResponse:
        """Generate a prompt based on the request, incorporating relevant context."""
        # Configure context injection
        config = ContextConfig(
            model_name=request.model_name,
            max_total_tokens=self._get_model_token_limit(request.model_name),
            max_context_tokens=self._get_context_token_limit(request.model_name),
            priority_threshold=0.3
        )

        # Get formatted context
        formatted_context, context_metadata = self.context_injection.select_and_format_contexts(
            query=request.goal,
            config=config,
            required_context_ids=request.required_context_ids
        )

        # Find appropriate template
        template = self._select_template(
            goal=request.goal,
            template_type=request.template_type
        )

        if not template:
            raise ValueError("No suitable template found")

        # Prepare variables with injected context
        variables = self._prepare_variables(
            base_variables=request.variables or {},
            formatted_context=formatted_context,
            template=template
        )

        # Generate the prompt
        prompt = self.template_engine.render_template(
            template_id=template.id,
            variables=variables
        )

        # Analyze token usage
        token_usage = self.context_injection.analyze_token_usage(prompt)

        # Create response
        response = PromptResponse(
            prompt=prompt,
            template_id=template.id,
            context_ids=[ctx["id"] for ctx in context_metadata["included_contexts"]],
            metadata={
                "goal": request.goal,
                "template_type": template.type,
                "context_metadata": context_metadata,
                **(request.metadata or {})
            },
            token_usage=token_usage,
            created_at=datetime.now()
        )

        return response

    def _get_model_token_limit(self, model_name: str) -> int:
        """Get token limit for specified model."""
        limits = {
            "gpt-3.5-turbo": 4096,
            "gpt-4": 8192,
            "gpt-4-32k": 32768
        }
        return limits.get(model_name, 4096)

    def _get_context_token_limit(self, model_name: str) -> int:
        """Get context token limit for specified model."""
        # Use about 50% of total tokens for context
        total_limit = self._get_model_token_limit(model_name)
        return total_limit // 2

    def _select_template(self, goal: str, template_type: Optional[str] = None) -> Optional[PromptTemplate]:
        """Select the most appropriate template based on goal and type."""
        templates = self.template_engine.find_templates(
            template_type=template_type,
            min_success_rate=0.5,
            active_only=True
        )

        if not templates:
            return None

<<<<<<< HEAD
        # Implement sophisticated template selection algorithm
        scored_templates = []

        for template in templates:
            score = 0.0
            reasons = []

            # Base score from success rate (0-40 points)
            success_score = template.success_rate * 40
            score += success_score
            reasons.append(f"success_rate:{template.success_rate:.2f}")

            # Goal similarity scoring (0-30 points)
            goal_similarity = self._calculate_goal_similarity(goal, template)
            score += goal_similarity * 30
            reasons.append(f"goal_similarity:{goal_similarity:.2f}")

            # Template recency bonus (0-10 points)
            if hasattr(template, 'last_used') and template.last_used:
                days_since_used = (datetime.now() - template.last_used).days
                recency_score = max(0, 10 - days_since_used)  # Decay over 10 days
                score += recency_score
                reasons.append(f"recency:{recency_score:.1f}")

            # Template complexity matching (0-10 points)
            complexity_match = self._calculate_complexity_match(goal, template)
            score += complexity_match * 10
            reasons.append(f"complexity:{complexity_match:.2f}")

            # Usage frequency bonus (0-10 points) - prefer frequently used templates
            if hasattr(template, 'usage_count') and template.usage_count:
                frequency_score = min(10, template.usage_count / 10)  # Cap at 10 uses
                score += frequency_score
                reasons.append(f"frequency:{frequency_score:.1f}")

            scored_templates.append({
                'template': template,
                'score': score,
                'reasons': reasons
            })

        # Sort by score and return best template
        scored_templates.sort(key=lambda x: x['score'], reverse=True)
        best_template = scored_templates[0]['template']

        logger.info(f"Selected template '{best_template.name}' with score {scored_templates[0]['score']:.1f} "
                   f"based on: {', '.join(scored_templates[0]['reasons'])}")

        return best_template
=======
        # TODO: Implement more sophisticated template selection
        # For now, return the template with highest success rate
        return max(templates, key=lambda t: t.success_rate)
>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1

    def _prepare_variables(self, base_variables: Dict, formatted_context: str, template: PromptTemplate) -> Dict:
        """Prepare variables for template rendering, incorporating formatted context."""
        variables = base_variables.copy()
        variables["context"] = formatted_context

        # Ensure all required variables are present
        missing_vars = set(template.variables or []) - set(variables.keys())
        if missing_vars:
            raise ValueError(f"Missing required variables: {missing_vars}")

        return variables

<<<<<<< HEAD
    def _calculate_goal_similarity(self, goal: str, template: PromptTemplate) -> float:
        """Calculate similarity between goal and template based on keywords and categories."""
        goal_lower = goal.lower()
        template_text = (template.name + " " + (template.description or "")).lower()

        # Keyword matching
        goal_words = set(goal_lower.split())
        template_words = set(template_text.split())

        # Calculate Jaccard similarity
        intersection = goal_words.intersection(template_words)
        union = goal_words.union(template_words)

        if not union:
            return 0.0

        similarity = len(intersection) / len(union)

        # Category matching bonus
        if hasattr(template, 'category') and template.category:
            category_keywords = {
                'coding': ['code', 'programming', 'function', 'class', 'api', 'debug'],
                'writing': ['write', 'content', 'text', 'article', 'blog', 'document'],
                'analysis': ['analyze', 'review', 'assess', 'evaluate', 'data'],
                'design': ['design', 'ui', 'ux', 'interface', 'layout'],
                'business': ['business', 'strategy', 'planning', 'management'],
                'research': ['research', 'study', 'investigate', 'explore']
            }

            category = template.category.lower()
            if category in category_keywords:
                category_words = set(category_keywords[category])
                category_matches = goal_words.intersection(category_words)
                if category_matches:
                    similarity += 0.2  # Category bonus

        return min(1.0, similarity)

    def _calculate_complexity_match(self, goal: str, template: PromptTemplate) -> float:
        """Calculate how well template complexity matches goal complexity."""
        goal_length = len(goal.split())
        template_complexity = getattr(template, 'complexity', 'medium')

        # Estimate goal complexity based on length and keywords
        if goal_length < 10:
            goal_complexity = 'simple'
        elif goal_length < 25:
            goal_complexity = 'medium'
        else:
            goal_complexity = 'complex'

        # Advanced keywords indicate higher complexity
        advanced_keywords = ['optimize', 'architecture', 'system', 'integration', 'scalability']
        if any(keyword in goal.lower() for keyword in advanced_keywords):
            goal_complexity = 'complex'

        # Calculate match score
        complexity_levels = {'simple': 1, 'medium': 2, 'complex': 3}
        template_level = complexity_levels.get(template_complexity, 2)
        goal_level = complexity_levels.get(goal_complexity, 2)

        # Perfect match gets 1.0, adjacent levels get 0.7, others get 0.3
        level_diff = abs(template_level - goal_level)
        if level_diff == 0:
            return 1.0
        elif level_diff == 1:
            return 0.7
        else:
            return 0.3

=======
>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1
    def record_success(self, template_id: str, context_ids: List[str], success: bool) -> None:
        """Record success/failure for template and update context relevance."""
        # Update template success rate
        self.template_engine.update_success_rate(template_id, success)

        # Update context relevance scores
        for context_id in context_ids:
            self.context_manager.update_relevance_scores(context_id)

    def create_conversation_context(self, 
                                  title: str,
                                  content: str,
                                  parent_id: Optional[str] = None,
                                  metadata: Optional[Dict] = None) -> str:
        """Create a new conversation context."""
        context = Context(
            id=str(uuid.uuid4()),
            type="conversation",
            title=title,
            content=content,
            parent_id=parent_id,
            metadata=metadata or {},
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        return self.context_manager.create_context(context)

    def create_strategic_context(self,
                               title: str,
                               content: str,
                               metadata: Optional[Dict] = None) -> str:
        """Create a new strategic context."""
        context = Context(
            id=str(uuid.uuid4()),
            type="strategic",
            title=title,
            content=content,
            metadata=metadata or {},
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        return self.context_manager.create_context(context)

    def maintain_system(self) -> Tuple[List[str], List[str]]:
        """Perform system maintenance tasks."""
        # Prune low-relevance contexts
        pruned_contexts = self.context_manager.prune_contexts(threshold=0.1)

        # Find underperforming templates
        underperforming = []
        templates = self.template_engine.find_templates(min_success_rate=None)
        for template in templates:
            if template.usage_count > 10 and template.success_rate < 0.3:
                underperforming.append(template.id)

        return pruned_contexts, underperforming

# EDIT START: Legacy alias for compatibility (must be at the very end of the file)
ScraperOrchestrator = PromptOrchestrator
# EDIT END