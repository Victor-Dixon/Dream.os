.PHONY: init lint test validate ci sweep overnight onboard prod-ready hooks update health backup package docker-build docker-push install clean

init:
	python -m pip install --upgrade pip
	pip install -r requirements.txt || true
	pip install -r requirements-dev.txt || true

install:
	./install.sh

docker-install:
	./install.sh --docker

docker-build:
	docker build -t dream-os:latest .

docker-run:
	docker run -d --name dream-os -p 8000:8000 -v $(PWD)/agent_workspaces:/app/agent_workspaces dream-os:latest

docker-compose-up:
	docker-compose up -d

docker-compose-down:
	docker-compose down

package:
	python -m build
	twine check dist/*

hooks:
	chmod +x scripts/hooks/pre-push.sh
	git config core.hooksPath scripts/hooks

lint:
	ruff check .
	black --check .
	isort --check-only .

format:
	black .
	isort .

validate:
	python scripts/validate_v2_compliance.py --rules config/v2_rules.yaml

test:
	pytest -q --maxfail=1 --disable-warnings --cov=scripts --cov=src --cov-fail-under=85

ci: lint validate test

update:
	python scripts/update.py update

health:
	python scripts/health_check.py --check

backup:
	python scripts/update.py backup

sweep:
	python tools/mode_sweep.py

overnight:
	python scripts/overnight/overnight_main.py

onboard:
	python cli.py --onboard --role-map production_ready

prod-ready:
	$(MAKE) ci && python cli.py --onboard --role-map production_ready --wrapup-only

monitor:
	python scripts/health_check.py --continuous --interval 60

logs:
	tail -f logs/*.log

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name ".coverage" -delete
	rm -rf .pytest_cache/
	rm -rf htmlcov/
	rm -rf dist/
	rm -rf build/
	rm -rf *.egg-info/

deep-clean: clean
	rm -rf agent_workspaces/*/cache/
	rm -rf logs/*.log
	rm -rf temp/
	rm -rf backups/

reset:
	$(MAKE) deep-clean
	rm -rf agent_workspaces/
	rm -rf data/
	rm -rf .env
	$(MAKE) init

help:
	@echo "Agent Cellphone V2 - Available commands:"
	@echo ""
	@echo "Installation & Setup:"
	@echo "  make install          - Install in native Python mode"
	@echo "  make docker-install   - Install with Docker"
	@echo "  make init             - Initialize development environment"
	@echo ""
	@echo "Docker Operations:"
	@echo "  make docker-build     - Build Docker image"
	@echo "  make docker-run       - Run container"
	@echo "  make docker-compose-up   - Start all services"
	@echo "  make docker-compose-down - Stop all services"
	@echo ""
	@echo "Development:"
	@echo "  make lint             - Run code linting"
	@echo "  make format           - Format code"
	@echo "  make test             - Run tests"
	@echo "  make validate         - Validate V2 compliance"
	@echo "  make ci               - Run full CI pipeline"
	@echo ""
	@echo "Operations:"
	@echo "  make update           - Update system to latest version"
	@echo "  make health           - Run health check"
	@echo "  make backup           - Create system backup"
	@echo "  make monitor          - Start health monitoring"
	@echo "  make logs             - View system logs"
	@echo ""
	@echo "Maintenance:"
	@echo "  make clean            - Clean build artifacts"
	@echo "  make deep-clean       - Clean all temporary files"
	@echo "  make reset            - Reset to clean state"
	@echo ""
	@echo "Legacy (V1 compatibility):"
	@echo "  make sweep            - Run mode sweep"
	@echo "  make overnight        - Run overnight operations"
	@echo "  make onboard          - Run onboarding"
	@echo "  make prod-ready       - Production readiness check"