# Start Here: Dream.os Quick Onboarding

<!-- SSOT Domain: documentation -->

Welcome! This guide gets you from zero to a working local swarm in the fastest, least confusing path.

## 1) Minimal thing to run (fastest path)

Use the 60-second Docker quickstart from the main README:

```bash
git clone <repository-url>
cd Dream.os
python setup.py --docker
python main.py --status
```

That is the smallest path to a healthy local baseline. From there, you can add optional services below.

## 2) Optional components (add only if you need them)

- **Discord bot**: Enables command-driven coordination.
- **Monitoring dashboard**: Grafana at `http://localhost:3000` (admin/admin123).
- **Web dashboard**: Swarm UI at `http://localhost:5000`.
- **API docs**: FastAPI docs at `http://localhost:8001/docs`.

Skip these until you want to validate specific workflows.

## 3) Expected workflow (what happens after setup)

1. **Check system status**:
   ```bash
   python main.py --status
   ```
2. **Start services**:
   ```bash
   python main.py --background
   ```
3. **Validate health**:
   ```bash
   python scripts/health_check.py --check
   ```
4. **Stop services when done**:
   ```bash
   python main.py --stop
   ```

## 4) Demo loop (1 start + 1 health check + 1 visual)

This gives a quick “is it alive?” signal without a long setup tour.

1. **Start services**:
   ```bash
   python main.py --background
   ```
2. **Confirm health**:
   ```bash
   python main.py --status
   ```
3. **View a dashboard**:
   - Local web UI: `http://localhost:5000`
   - Static demo HTML: `sites/weareswarm.online/swarm-activity-dashboard.html`

## 5) Security note (public repo safety)

The `.deploy_credentials/` directory is **template-only**. Example files are committed for reference, while
real credentials are excluded by `.gitignore`. Copy the example files locally if you need them:

```bash
cp .deploy_credentials/sites.example.json .deploy_credentials/sites.json
cp .deploy_credentials/blogging_api.example.json .deploy_credentials/blogging_api.json
```

If you ever committed real credentials, rotate them immediately.

## 6) Next steps

- Read the full [README](../README.md)
- Review the [Platform Setup Guide](../PLATFORM_SETUP.md)
- Explore the deeper [Quick Start](../QUICKSTART.md)
