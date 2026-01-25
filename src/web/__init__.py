"""
Web Layer - Flask Application
==============================

<!-- SSOT Domain: web -->

Main Flask application initialization and blueprint registration.
V2 Compliance: < 300 lines, single responsibility.
"""

from flask import Flask


def _safe_import(path: str, attr: str):
    try:
        module = __import__(path, fromlist=[attr])
        return getattr(module, attr)
    except Exception:
        return None


# Import blueprints (best-effort to keep tests lightweight)
analysis_bp = _safe_import("src.web.analysis_routes", "analysis_bp")
task_bp = _safe_import("src.web.task_routes", "task_bp")
contract_bp = _safe_import("src.web.contract_routes", "contract_bp")
core_bp = _safe_import("src.web.core_routes", "core_bp")
workflow_bp = _safe_import("src.web.workflow_routes", "workflow_bp")
services_bp = _safe_import("src.web.services_routes", "services_bp")
coordination_bp = _safe_import("src.web.coordination_routes", "coordination_bp")
integrations_bp = _safe_import("src.web.integrations_routes", "integrations_bp")
monitoring_bp = _safe_import("src.web.monitoring_routes", "monitoring_bp")
scheduler_bp = _safe_import("src.web.scheduler_routes", "scheduler_bp")
vision_bp = _safe_import("src.web.vision_routes", "vision_bp")
engines_bp = _safe_import("src.web.engines_routes", "engines_bp")
repository_merge_bp = _safe_import("src.web.repository_merge_routes", "repository_merge_bp")
agent_management_bp = _safe_import("src.web.agent_management_routes", "agent_management_bp")
execution_coordinator_bp = _safe_import("src.web.execution_coordinator_routes", "execution_coordinator_bp")
manager_registry_bp = _safe_import("src.web.manager_registry_routes", "manager_registry_bp")
results_processor_bp = _safe_import("src.web.results_processor_routes", "results_processor_bp")
swarm_intelligence_bp = _safe_import("src.web.swarm_intelligence_routes", "swarm_intelligence_bp")
service_integration_bp = _safe_import("src.web.service_integration_routes", "service_integration_bp")
manager_operations_bp = _safe_import("src.web.manager_operations_routes", "manager_operations_bp")
assignment_bp = _safe_import("src.web.assignment_routes", "assignment_bp")
chat_presence_bp = _safe_import("src.web.chat_presence_routes", "chat_presence_bp")
pipeline_bp = _safe_import("src.web.pipeline_routes", "pipeline_bp")
messaging_bp = _safe_import("src.web.messaging_routes", "messaging_bp")
vector_db_bp = _safe_import("src.web.vector_database.routes", "vector_db_bp")
message_bp = _safe_import("src.web.vector_database.message_routes", "message_bp")
discord_bp = _safe_import("src.web.discord_routes", "discord_bp")
ai_training_bp = _safe_import("src.web.ai_training_routes", "ai_training_bp")
architecture_bp = _safe_import("src.web.architecture_routes", "architecture_bp")
validation_bp = _safe_import("src.web.validation_routes", "validation_bp")


def create_app() -> Flask:
    """
    Create and configure Flask application.

    Returns:
        Configured Flask application instance
    """
    app = Flask(__name__)

    # Register blueprints (skip missing/optional)
    for blueprint in [
        task_bp,
        contract_bp,
        core_bp,
        workflow_bp,
        services_bp,
        coordination_bp,
        integrations_bp,
        monitoring_bp,
        scheduler_bp,
        vision_bp,
        engines_bp,
        repository_merge_bp,
        agent_management_bp,
        execution_coordinator_bp,
        manager_registry_bp,
        results_processor_bp,
        swarm_intelligence_bp,
        service_integration_bp,
        manager_operations_bp,
        assignment_bp,
        chat_presence_bp,
        pipeline_bp,
        messaging_bp,
        vector_db_bp,
        message_bp,
        discord_bp,
        ai_training_bp,
        architecture_bp,
        validation_bp,
        analysis_bp,
    ]:
        if blueprint is not None:
            app.register_blueprint(blueprint)

    return app


def register_all_blueprints(app: Flask) -> None:
    """
    Register all blueprints with Flask app.

    Args:
        app: Flask application instance
    """
    for blueprint in [
        task_bp,
        contract_bp,
        core_bp,
        workflow_bp,
        services_bp,
        coordination_bp,
        integrations_bp,
        monitoring_bp,
        scheduler_bp,
        vision_bp,
        engines_bp,
        repository_merge_bp,
        agent_management_bp,
        execution_coordinator_bp,
        manager_registry_bp,
        results_processor_bp,
        swarm_intelligence_bp,
        service_integration_bp,
        manager_operations_bp,
        assignment_bp,
        chat_presence_bp,
        pipeline_bp,
        messaging_bp,
        vector_db_bp,
        message_bp,
        discord_bp,
        ai_training_bp,
        architecture_bp,
        validation_bp,
        analysis_bp,
    ]:
        if blueprint is not None:
            app.register_blueprint(blueprint)
