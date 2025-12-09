"""
Web Layer - Flask Application
==============================

<!-- SSOT Domain: web -->

Main Flask application initialization and blueprint registration.
V2 Compliance: < 300 lines, single responsibility.
"""

from flask import Flask

# Import blueprints
from src.web.task_routes import task_bp
from src.web.contract_routes import contract_bp
from src.web.core_routes import core_bp
from src.web.workflow_routes import workflow_bp
from src.web.services_routes import services_bp
from src.web.coordination_routes import coordination_bp
from src.web.integrations_routes import integrations_bp
from src.web.monitoring_routes import monitoring_bp
from src.web.scheduler_routes import scheduler_bp
from src.web.vision_routes import vision_bp
from src.web.engines_routes import engines_bp
from src.web.repository_merge_routes import repository_merge_bp
from src.web.agent_management_routes import agent_management_bp
from src.web.execution_coordinator_routes import execution_coordinator_bp
from src.web.manager_registry_routes import manager_registry_bp
from src.web.results_processor_routes import results_processor_bp
from src.web.swarm_intelligence_routes import swarm_intelligence_bp
from src.web.service_integration_routes import service_integration_bp
from src.web.manager_operations_routes import manager_operations_bp
from src.web.assignment_routes import assignment_bp
from src.web.chat_presence_routes import chat_presence_bp
from src.web.pipeline_routes import pipeline_bp
from src.web.messaging_routes import messaging_bp
from src.web.vector_database.routes import vector_db_bp
from src.web.vector_database.message_routes import message_bp
from src.web.discord_routes import discord_bp
from src.web.ai_training_routes import ai_training_bp
from src.web.architecture_routes import architecture_bp
from src.web.validation_routes import validation_bp
from src.web.analysis_routes import analysis_bp


def create_app() -> Flask:
    """
    Create and configure Flask application.

    Returns:
        Configured Flask application instance
    """
    app = Flask(__name__)

    # Register blueprints
    app.register_blueprint(task_bp)
    app.register_blueprint(contract_bp)
    app.register_blueprint(core_bp)
    app.register_blueprint(workflow_bp)
    app.register_blueprint(services_bp)
    app.register_blueprint(coordination_bp)
    app.register_blueprint(integrations_bp)
    app.register_blueprint(monitoring_bp)
    app.register_blueprint(scheduler_bp)
    app.register_blueprint(vision_bp)
    app.register_blueprint(engines_bp)
    app.register_blueprint(repository_merge_bp)
    app.register_blueprint(agent_management_bp)
    app.register_blueprint(execution_coordinator_bp)
    app.register_blueprint(manager_registry_bp)
    app.register_blueprint(results_processor_bp)
    app.register_blueprint(swarm_intelligence_bp)
    app.register_blueprint(service_integration_bp)
    app.register_blueprint(manager_operations_bp)
    app.register_blueprint(assignment_bp)
    app.register_blueprint(chat_presence_bp)
    app.register_blueprint(pipeline_bp)
    app.register_blueprint(messaging_bp)
    app.register_blueprint(vector_db_bp)
    app.register_blueprint(message_bp)
    app.register_blueprint(discord_bp)
    app.register_blueprint(ai_training_bp)
    app.register_blueprint(architecture_bp)
    app.register_blueprint(validation_bp)
    app.register_blueprint(analysis_bp)

    return app


def register_all_blueprints(app: Flask) -> None:
    """
    Register all blueprints with Flask app.

    Args:
        app: Flask application instance
    """
    app.register_blueprint(task_bp)
    app.register_blueprint(contract_bp)
    app.register_blueprint(core_bp)
    app.register_blueprint(workflow_bp)
    app.register_blueprint(services_bp)
    app.register_blueprint(coordination_bp)
    app.register_blueprint(integrations_bp)
    app.register_blueprint(monitoring_bp)
    app.register_blueprint(scheduler_bp)
    app.register_blueprint(vision_bp)
    app.register_blueprint(engines_bp)
    app.register_blueprint(repository_merge_bp)
    app.register_blueprint(agent_management_bp)
    app.register_blueprint(execution_coordinator_bp)
    app.register_blueprint(manager_registry_bp)
    app.register_blueprint(results_processor_bp)
    app.register_blueprint(swarm_intelligence_bp)
    app.register_blueprint(service_integration_bp)
    app.register_blueprint(manager_operations_bp)
    app.register_blueprint(assignment_bp)
    app.register_blueprint(chat_presence_bp)
    app.register_blueprint(pipeline_bp)
    app.register_blueprint(messaging_bp)
    app.register_blueprint(vector_db_bp)
    app.register_blueprint(message_bp)
    app.register_blueprint(discord_bp)
    app.register_blueprint(ai_training_bp)
    app.register_blueprint(architecture_bp)
    app.register_blueprint(validation_bp)
    app.register_blueprint(analysis_bp)
