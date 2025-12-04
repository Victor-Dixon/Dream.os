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
from src.web.vector_database.routes import vector_db_bp
from src.web.vector_database.message_routes import message_bp


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
    app.register_blueprint(vector_db_bp)
    app.register_blueprint(message_bp)

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
    app.register_blueprint(vector_db_bp)
    app.register_blueprint(message_bp)
