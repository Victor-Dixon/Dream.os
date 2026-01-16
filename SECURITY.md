# Security Policy

## Reporting a Vulnerability

If you discover a security issue, please **do not** open a public issue. Instead:

- Email: security@dreamos.local (placeholder)
- Include: reproduction steps, impact, and any relevant logs

## Secrets Handling

- Real credentials must live in `.deploy_credentials/` (ignored by `.gitignore`).
- Templates live in `.deploy_credentials.example/` and may be committed.
- Never commit `.env` files or API keys.

Thank you for helping keep the project safe.
