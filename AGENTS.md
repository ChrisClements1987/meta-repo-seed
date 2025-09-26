# Agent Instructions for Business-in-a-Box Platform

## Commands
- **Test**: `python -m pytest` (all tests), `python -m pytest tests/unit/test_filename.py::TestClass::test_method` (single test)
- **Coverage**: `python -m pytest --cov=seeding --cov=src --cov-report=term-missing`
- **Business CLI**: `python -m src.cli.business_commands deploy-business --profile=startup-basic --dry-run` (test business deployment)
- **Product Launch**: `python -m src.cli.business_commands launch-product --stack=nextjs --name=test-app --dry-run` (test product launch)
- **Legacy CLI**: `python seeding.py --dry-run --verbose` (legacy repository scaffolding)
- **Linting**: `flake8 . --max-line-length=127`, `black --line-length=127 .`, `isort .`

## Architecture
- **Business CLI**: `src/cli/business_commands.py` - Business-focused commands for organizational deployment (deploy-business, launch-product, start-onboarding, validate-deployment)
- **Organization Blueprints**: `src/blueprints/` - Multi-repo organizational deployment with parser, orchestrator, and business profiles
- **Product Templates**: `src/templates/` - Production-ready app templates with CI/CD (Next.js, Python API, Node API, React SPA, Static Site)
- **PaaS Providers**: `src/providers/` - Deployment integration (Vercel, Netlify, Cloudflare Pages, Fly.io)
- **Legacy System**: `seeding.py` - Original repository scaffolding (backward compatibility)
- **Testing**: pytest with 119 unit tests, GitHub Actions CI/CD with multi-Python testing (3.8-3.12)

## Code Style
- **Python**: PEP 8 style, type hints required (typing module imports), comprehensive docstrings
- **Error Handling**: Use specific exceptions, input validation/sanitization for security (path traversal protection)
- **Imports**: Standard library first, third-party second, local imports last
- **Logging**: Use `logging` module with proper levels, structured error messages
- **Security**: Sanitize all user inputs, validate project names with regex, prevent path traversal attacks
- **Functions**: Pure functions preferred, idempotent operations, clear separation of concerns

## Development Notes  
- Project uses branch protection (develop→main workflow), idempotent design allows safe re-runs
- Test markers: `@pytest.mark.unit`, `@pytest.mark.integration`, `@pytest.mark.github`, `@pytest.mark.slow`, `@pytest.mark.network`

## Business-in-a-Box Features
- **Target Market**: Startups, charities, non-profits, and SMBs needing professional infrastructure
- **Core Value**: Deploy complete organizational infrastructure in <10 minutes, launch products in <10 minutes
- **Business Profiles**: startup-basic, charity-nonprofit, smb-standard, consulting-firm (startup-basic implemented)
- **Product Stacks**: Next.js, Python API, Node API, React SPA, Static Site (all implemented)
- **Deployment**: Multi-tier portfolio architecture with professional governance, CI/CD, and PaaS integration
