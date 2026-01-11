#!/usr/bin/env python3
"""
AI Context Engine Context Processors
===================================

Context processing logic for different context types.

<!-- SSOT Domain: ai_context -->

Navigation References:
├── Related Files:
│   ├── Main Engine → ai_context_engine.py
│   ├── Data Models → models.py
│   ├── Suggestion Generators → suggestion_generators.py
│   └── Risk Calculator → src/services/risk_analytics/risk_calculator_service.py
├── Documentation:
│   └── Phase 5 Architecture → docs/PHASE5_AI_CONTEXT_ENGINE.md
└── Testing:
    └── Integration Tests → tests/integration/test_ai_context_engine.py

Classes:
- ContextProcessor: Base class for context processors
- TradingContextProcessor: Handles trading context processing
- CollaborationContextProcessor: Handles collaboration context
- AnalysisContextProcessor: Handles analytical context
- RiskContextProcessor: Handles risk-focused context
"""

import time
from typing import List, Dict, Any, Optional
from datetime import datetime
from pathlib import Path
import logging

from .models import ContextSession, ContextSuggestion
from .suggestion_generators import SuggestionGenerators
from src.services.risk_analytics.risk_calculator_service import RiskCalculatorService

logger = logging.getLogger(__name__)


class ContextProcessor:
    """
    Base class for context processors.

    Navigation:
    ├── Subclasses: TradingContextProcessor, CollaborationContextProcessor, etc.
    ├── Used by: AIContextEngine._process_context()
    └── Related: ContextSession, ContextSuggestion
    """

    def __init__(self):
        """Initialize the context processor."""
        self.suggestion_generators = SuggestionGenerators()

    async def process(self, session: ContextSession) -> List[ContextSuggestion]:
        """
        Process context and generate suggestions.

        Args:
            session: The context session to process

        Returns:
            List of context suggestions
        """
        raise NotImplementedError("Subclasses must implement process()")


class TradingContextProcessor(ContextProcessor):
    """
    Processes trading context with risk integration.

    Navigation:
    ├── Used by: AIContextEngine._process_context()
    ├── Depends on: RiskCalculatorService, SuggestionGenerators
    └── Related: trading_robot data structures, market data APIs
    """

    def __init__(self):
        """Initialize trading context processor."""
        super().__init__()
        self.risk_calculator = RiskCalculatorService()

    async def process(self, session: ContextSession) -> List[ContextSuggestion]:
        """
        Process trading context with risk integration.

        Navigation:
        ├── Calls: RiskCalculatorService.calculate_comprehensive_risk_metrics()
        ├── Uses: SuggestionGenerators.generate_risk_suggestions()
        └── Related: TradingRobotApp portfolio data, market volatility indicators
        """
        suggestions = []

        # Extract trading data
        context = session.context_data
        positions = context.get('positions', [])

        # Calculate risk metrics if we have position data
        if positions:
            try:
                # Convert positions to returns for risk calculation
                returns = self._extract_returns_from_positions(positions)
                if len(returns) >= 30:
                    risk_metrics = self.risk_calculator.calculate_comprehensive_risk_metrics(
                        np.array(returns),
                        np.array([p.get('equity', 10000) for p in positions])
                    )
                    session.risk_metrics = risk_metrics

                    # Generate risk-based suggestions
                    risk_suggestions = await self.suggestion_generators.generate_risk_suggestions(
                        risk_metrics, context, session.session_id)
                    suggestions.extend(risk_suggestions)

            except Exception as e:
                logger.error(f"Risk calculation error: {e}")

        # Generate trading-specific suggestions
        trading_suggestions = await self.suggestion_generators.generate_trading_suggestions(
            context, session.session_id)
        suggestions.extend(trading_suggestions)

        return suggestions

    def _extract_returns_from_positions(self, positions: List[Dict[str, Any]]) -> List[float]:
        """
        Extract return series from position data.

        Navigation:
        ├── Used by: process()
        └── Related: TradingRobotApp position data structures
        """
        returns = []
        for position in positions:
            if 'return' in position:
                returns.append(position['return'])
            elif 'pnl' in position and 'initial_value' in position:
                initial = position['initial_value']
                if initial > 0:
                    returns.append(position['pnl'] / initial)

        return returns if returns else [0.0]


class CollaborationContextProcessor(ContextProcessor):
    """
    Processes collaborative context for real-time collaboration.

    Navigation:
    ├── Used by: AIContextEngine._process_context()
    ├── Related: WebSocket collaboration features, user session management
    └── Documentation: docs/PHASE5_AI_CONTEXT_ENGINE.md#collaboration-features
    """

    async def process(self, session: ContextSession) -> List[ContextSuggestion]:
        """
        Process collaborative context for real-time collaboration.

        Navigation:
        ├── Related: ai_context_websocket.py collaboration features
        └── Uses: session collaborators data, current activity tracking
        """
        context = session.context_data
        collaborators = context.get('collaborators', [])
        current_activity = context.get('current_activity', '')

        suggestions = []

        # Generate collaboration suggestions
        if len(collaborators) > 1:
            collab_suggestion = ContextSuggestion(
                suggestion_id=f"collab_{session.session_id}_{int(time.time())}",
                session_id=session.session_id,
                suggestion_type="collaboration",
                confidence_score=0.85,
                content={
                    "action": "suggest_collaborative_action",
                    "collaborators": collaborators,
                    "suggestion": f"Consider coordinating with {len(collaborators)} other collaborators on {current_activity}"
                },
                reasoning="Multiple collaborators detected - suggesting coordination opportunities",
                timestamp=datetime.now()
            )
            suggestions.append(collab_suggestion)

        return suggestions


class AnalysisContextProcessor(ContextProcessor):
    """
    Processes analytical context for intelligent insights.

    Navigation:
    ├── Used by: AIContextEngine._process_context()
    ├── Depends on: PatternAnalysisEngine from core.analytics.intelligence
    └── Related: data analysis workflows, pattern recognition systems
    """

    def analyze_directory_context(self, context_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        AI-powered analysis of directory patterns and usage for intelligent recommendations.

        Args:
            context_data: Dictionary containing directory analysis parameters

        Returns:
            Dictionary with analysis results and recommendations
        """
        directory_path = context_data.get("directory_path", "")
        directory_type = context_data.get("directory_type", "unknown")

        # Perform pattern analysis
        file_patterns = self._analyze_file_patterns(directory_path)
        activity_level = self._assess_activity_level(directory_path)
        risk_factors = self._identify_risk_factors(directory_path)

        # Generate confidence score based on data completeness
        confidence = self._calculate_confidence_score(file_patterns, activity_level)

        return {
            "file_patterns": file_patterns,
            "activity_level": activity_level,
            "risk_factors": risk_factors,
            "confidence": confidence,
            "directory_type": directory_type,
            "analysis_timestamp": context_data.get("timestamp", "")
        }

    def _analyze_file_patterns(self, directory_path: str) -> Dict[str, Any]:
        """Analyze file patterns in directory"""
        try:
            path = Path(directory_path)
            if not path.exists():
                return {"error": "directory_not_found"}

            files = list(path.rglob("*"))
            total_files = len([f for f in files if f.is_file()])

            # Basic pattern analysis
            extensions = {}
            large_files = 0
            config_files = 0

            for file in files:
                if file.is_file():
                    ext = file.suffix.lower()
                    extensions[ext] = extensions.get(ext, 0) + 1

                    # Check for large files (>10MB)
                    if file.stat().st_size > 10 * 1024 * 1024:
                        large_files += 1

                    # Check for config files
                    if file.name in ['status.json', 'config.json', '.env', 'settings.py']:
                        config_files += 1

            return {
                "total_files": total_files,
                "file_extensions": extensions,
                "large_files_count": large_files,
                "config_files_count": config_files,
                "duplicate_configs": config_files
            }
        except Exception as e:
            return {"error": str(e)}

    def _assess_activity_level(self, directory_path: str) -> str:
        """Assess activity level based on recent modifications"""
        try:
            path = Path(directory_path)
            if not path.exists():
                return "unknown"

            # Check recent file modifications (last 30 days)
            recent_modifications = 0
            total_files = 0
            thirty_days_ago = datetime.now().timestamp() - (30 * 24 * 60 * 60)

            for file in path.rglob("*"):
                if file.is_file():
                    total_files += 1
                    if file.stat().st_mtime > thirty_days_ago:
                        recent_modifications += 1

            if total_files == 0:
                return "empty"

            activity_ratio = recent_modifications / total_files

            if activity_ratio > 0.5:
                return "high_activity"
            elif activity_ratio > 0.2:
                return "moderate_activity"
            elif activity_ratio > 0.05:
                return "low_activity"
            else:
                return "inactive"

        except Exception:
            return "unknown"

    def _identify_risk_factors(self, directory_path: str) -> List[Dict[str, Any]]:
        """Identify potential risk factors in directory"""
        risks = []

        try:
            path = Path(directory_path)
            if not path.exists():
                return risks

            # Check for large files
            large_files = []
            for file in path.rglob("*"):
                if file.is_file() and file.stat().st_size > 50 * 1024 * 1024:  # 50MB
                    large_files.append(file.name)

            if large_files:
                risks.append({
                    "type": "large_files",
                    "severity": "medium",
                    "details": f"Found {len(large_files)} large files: {', '.join(large_files[:3])}"
                })

            # Check for old temporary files
            old_temp_files = []
            thirty_days_ago = datetime.now().timestamp() - (30 * 24 * 60 * 60)

            for file in path.rglob("*"):
                if file.is_file() and file.stat().st_mtime < thirty_days_ago:
                    if any(temp_indicator in file.name.lower() for temp_indicator in ['temp', 'tmp', 'cache', 'old']):
                        old_temp_files.append(file.name)

            if old_temp_files:
                risks.append({
                    "type": "old_temp_files",
                    "severity": "low",
                    "details": f"Found {len(old_temp_files)} old temporary files"
                })

        except Exception as e:
            risks.append({
                "type": "analysis_error",
                "severity": "low",
                "details": f"Risk analysis failed: {str(e)}"
            })

        return risks

    def _calculate_confidence_score(self, file_patterns: Dict, activity_level: str) -> float:
        """Calculate confidence score for analysis results"""
        confidence = 0.5  # Base confidence

        # Higher confidence with more data
        if file_patterns.get("total_files", 0) > 10:
            confidence += 0.2

        # Higher confidence with clear activity patterns
        if activity_level != "unknown":
            confidence += 0.2

        # Higher confidence with diverse file types
        if len(file_patterns.get("file_extensions", {})) > 3:
            confidence += 0.1

        return min(confidence, 1.0)

    async def process(self, session: ContextSession) -> List[ContextSuggestion]:
        """
        Process analytical context for intelligent insights.

        Navigation:
        ├── Uses: PatternAnalysisEngine.analyze_patterns()
        └── Related: data visualization components, analytical dashboards
        """
        from src.core.analytics.intelligence.pattern_analysis_engine import PatternAnalysisEngine

        context = session.context_data
        data_points = context.get('data_points', [])

        if not data_points:
            return []

        # Use pattern analysis for insights
        try:
            pattern_analyzer = PatternAnalysisEngine()
            patterns = await pattern_analyzer.analyze_patterns(data_points)

            if patterns:
                analysis_suggestion = ContextSuggestion(
                    suggestion_id=f"analysis_{session.session_id}_{int(time.time())}",
                    session_id=session.session_id,
                    suggestion_type="insight",
                    confidence_score=0.78,
                    content={
                        "action": "show_pattern_insights",
                        "patterns": patterns,
                        "data_points": len(data_points)
                    },
                    reasoning=f"Pattern analysis detected {len(patterns)} significant patterns in {len(data_points)} data points",
                    timestamp=datetime.now()
                )
                return [analysis_suggestion]

        except Exception as e:
            logger.error(f"Pattern analysis error: {e}")

        return []


class RiskContextProcessor(ContextProcessor):
    """
    Processes risk-focused context.

    Navigation:
    ├── Used by: AIContextEngine._process_context()
    ├── Related: Risk monitoring dashboards, compliance systems
    └── Documentation: docs/PHASE5_AI_CONTEXT_ENGINE.md#risk-monitoring
    """

    async def process(self, session: ContextSession) -> List[ContextSuggestion]:
        """
        Process risk-focused context.

        Navigation:
        ├── Related: risk_websocket_server.py real-time risk streaming
        └── Uses: risk indicators, monitoring thresholds
        """
        context = session.context_data
        risk_indicators = context.get('risk_indicators', [])

        suggestions = []

        # Generate risk monitoring suggestions
        if risk_indicators:
            risk_suggestion = ContextSuggestion(
                suggestion_id=f"risk_monitor_{session.session_id}_{int(time.time())}",
                session_id=session.session_id,
                suggestion_type="risk_alert",
                confidence_score=0.92,
                content={
                    "action": "enhance_risk_monitoring",
                    "indicators": risk_indicators,
                    "recommendation": "Consider implementing additional risk monitoring for these indicators"
                },
                reasoning=f"Risk context detected with {len(risk_indicators)} risk indicators requiring attention",
                timestamp=datetime.now()
            )
            suggestions.append(risk_suggestion)

        return suggestions


class UXContextProcessor(ContextProcessor):
    """
    Processes UX context for hero sections and web interactions.

    Navigation:
    ├── Used by: AIContextEngine._process_context()
    ├── Depends on: SuggestionGenerators, hero section data
    └── Related: web hero components, user interaction tracking
    """

    def __init__(self):
        """Initialize UX context processor."""
        super().__init__()
        self.hero_context_types = {
            'gaming': ['ariajet', 'gaming_interaction', 'game_performance'],
            'business': ['prismblossom', 'business_metrics', 'consulting_focus'],
            'sports': ['crosbyultimate', 'event_engagement', 'community_focus']
        }

    async def process(self, session: ContextSession) -> List[ContextSuggestion]:
        """
        Process UX context for hero sections and generate AI-powered suggestions.

        Args:
            session: The UX context session to process

        Returns:
            List of UX context suggestions for hero sections
        """
        context = session.context_data
        user_interactions = context.get('user_interactions', [])
        hero_type = context.get('hero_type', 'general')
        engagement_metrics = context.get('engagement_metrics', {})

        suggestions = []

        # Generate hero personalization suggestions
        if hero_type in self.hero_context_types:
            personalization_suggestion = await self._generate_hero_personalization(
                session, hero_type, user_interactions, engagement_metrics
            )
            if personalization_suggestion:
                suggestions.append(personalization_suggestion)

        # Generate real-time adaptation suggestions
        if user_interactions:
            adaptation_suggestion = await self._generate_real_time_adaptation(
                session, user_interactions, engagement_metrics
            )
            if adaptation_suggestion:
                suggestions.append(adaptation_suggestion)

        # Generate predictive content suggestions
        if engagement_metrics:
            predictive_suggestion = await self._generate_predictive_content(
                session, engagement_metrics, hero_type
            )
            if predictive_suggestion:
                suggestions.append(predictive_suggestion)

        return suggestions

    async def _generate_hero_personalization(
        self, session: ContextSession, hero_type: str, user_interactions: List[Dict],
        engagement_metrics: Dict[str, Any]
    ) -> Optional[ContextSuggestion]:
        """Generate hero personalization suggestions based on user behavior."""

        interaction_count = len(user_interactions)
        engagement_score = engagement_metrics.get('score', 0.5)

        # Determine personalization strategy based on hero type and engagement
        if hero_type == 'gaming' and engagement_score > 0.7:
            personalization = {
                'strategy': 'gaming_enthusiast',
                'animations': ['accelerated_pixel_float', 'enhanced_glow_effects'],
                'content': 'Show advanced gaming features and community stats'
            }
        elif hero_type == 'business' and interaction_count > 3:
            personalization = {
                'strategy': 'business_professional',
                'animations': ['accelerated_growth_charts', 'professional_network'],
                'content': 'Highlight ROI metrics and consulting expertise'
            }
        elif hero_type == 'sports' and engagement_score > 0.6:
            personalization = {
                'strategy': 'sports_enthusiast',
                'animations': ['dynamic_frisbee_physics', 'crowd_energy'],
                'content': 'Show tournament highlights and community events'
            }
        else:
            personalization = {
                'strategy': 'general_engagement',
                'animations': ['standard_pulse', 'gentle_float'],
                'content': 'Show general features and call-to-action'
            }

        return ContextSuggestion(
            suggestion_id=f"ux_personalize_{session.session_id}_{int(time.time())}",
            session_id=session.session_id,
            suggestion_type="ux_personalization",
            confidence_score=min(0.95, 0.7 + (engagement_score * 0.3)),
            content={
                'hero_type': hero_type,
                'personalization': personalization,
                'engagement_score': engagement_score,
                'interaction_count': interaction_count,
                'action': 'apply_hero_personalization'
            },
            reasoning=f"UX context analysis shows {hero_type} hero with {engagement_score:.2f} engagement score, recommending {personalization['strategy']} personalization",
            timestamp=datetime.now()
        )

    async def _generate_real_time_adaptation(
        self, session: ContextSession, user_interactions: List[Dict],
        engagement_metrics: Dict[str, Any]
    ) -> Optional[ContextSuggestion]:
        """Generate real-time adaptation suggestions based on user behavior."""

        recent_interactions = user_interactions[-5:]  # Last 5 interactions
        scroll_patterns = [i for i in recent_interactions if i.get('type') == 'scroll']
        click_patterns = [i for i in recent_interactions if i.get('type') == 'click']

        # Analyze interaction patterns for real-time adaptation
        if len(scroll_patterns) > 2 and engagement_metrics.get('time_on_page', 0) > 30:
            return ContextSuggestion(
                suggestion_id=f"ux_adapt_scroll_{session.session_id}_{int(time.time())}",
                session_id=session.session_id,
                suggestion_type="real_time_adaptation",
                confidence_score=0.88,
                content={
                    'adaptation_type': 'scroll_engagement',
                    'action': 'accelerate_animations',
                    'reason': 'User showing deep engagement with scroll behavior',
                    'suggested_changes': {
                        'animation_speed': 'increase_25_percent',
                        'content_reveal': 'progressive_unveil',
                        'interactive_elements': 'activate_additional_ctas'
                    }
                },
                reasoning="Scroll pattern analysis indicates high engagement, suggesting animation acceleration and progressive content reveals",
                timestamp=datetime.now()
            )

        elif len(click_patterns) > 1:
            return ContextSuggestion(
                suggestion_id=f"ux_adapt_click_{session.session_id}_{int(time.time())}",
                session_id=session.session_id,
                suggestion_type="real_time_adaptation",
                confidence_score=0.82,
                content={
                    'adaptation_type': 'click_interaction',
                    'action': 'enhance_interactivity',
                    'reason': 'User actively engaging with interactive elements',
                    'suggested_changes': {
                        'hover_effects': 'amplify_feedback',
                        'click_animations': 'add_success_feedback',
                        'related_elements': 'highlight_connections'
                    }
                },
                reasoning="Click interaction pattern detected, recommending enhanced interactivity and feedback systems",
                timestamp=datetime.now()
            )

        return None

    async def _generate_predictive_content(
        self, session: ContextSession, engagement_metrics: Dict[str, Any], hero_type: str
    ) -> Optional[ContextSuggestion]:
        """Generate predictive content suggestions based on engagement patterns."""

        time_on_page = engagement_metrics.get('time_on_page', 0)
        content_views = engagement_metrics.get('content_views', 0)
        interaction_rate = engagement_metrics.get('interaction_rate', 0)

        # Predict content preferences based on engagement
        if time_on_page > 60 and interaction_rate > 0.3:
            # High engagement user - suggest advanced content
            if hero_type == 'gaming':
                predictive_content = {
                    'content_type': 'advanced_gaming_features',
                    'elements': ['game_engine_demos', 'developer_tools', 'community_showcase']
                }
            elif hero_type == 'business':
                predictive_content = {
                    'content_type': 'detailed_business_metrics',
                    'elements': ['case_studies', 'roi_calculators', 'consultation_cta']
                }
            elif hero_type == 'sports':
                predictive_content = {
                    'content_type': 'tournament_highlights',
                    'elements': ['live_scores', 'player_profiles', 'event_schedule']
                }
            else:
                predictive_content = {
                    'content_type': 'premium_features',
                    'elements': ['advanced_demos', 'detailed_specifications', 'contact_forms']
                }

            return ContextSuggestion(
                suggestion_id=f"ux_predict_content_{session.session_id}_{int(time.time())}",
                session_id=session.session_id,
                suggestion_type="predictive_content",
                confidence_score=0.85,
                content={
                    'prediction': predictive_content,
                    'engagement_indicators': {
                        'time_on_page': time_on_page,
                        'interaction_rate': interaction_rate,
                        'content_views': content_views
                    },
                    'action': 'load_predictive_content'
                },
                reasoning=f"High engagement detected ({time_on_page}s, {interaction_rate:.2f} interaction rate), predicting interest in {predictive_content['content_type']}",
                timestamp=datetime.now()
            )

        return None