## Local Development

Start infrastructure and API:

```bash
docker compose up --build
curl http://localhost:8000/v1/health
curl -X POST http://localhost:8000/v1/workflows \
  -H "Content-Type: application/json" \
  -d '{"repository_url":"https://github.com/pallets/flask"}'
curl http://localhost:8000/v1/workflows
curl http://localhost:8000/metrics

## GitHub Authentication

For private repositories, create a GitHub Personal Access Token.

Create a local `.env` file:

```env
GITHUB_TOKEN=your_token_here

## Production Readiness

ADWE currently includes:

- FastAPI backend
- PostgreSQL persistence
- Redis service
- Docker Compose local stack
- Alembic database migrations
- LangGraph workflow orchestration
- Repository architecture analysis
- Implementation planning agent
- Code modification proposal agent
- Patch application workflow
- Test execution service
- Pull request creation scaffolding
- Audit event persistence
- Prometheus metrics endpoint
- Request ID middleware
- GitHub Actions CI

Planned next features:

- Redis-backed worker queue
- OpenTelemetry tracing
- Real LLM-powered planning
- GitHub branch push support
- End-to-end pull request automation
- Role-based access control
