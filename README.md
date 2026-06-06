# Agentic Development Workflow Engine

![CI](https://github.com/jennasilvera/adwe/actions/workflows/ci.yml/badge.svg)

Agentic Development Workflow Engine (ADWE) is a production-oriented platform for repository analysis, implementation planning, workflow orchestration, audit logging, and pull request automation.

## Architecture

The system consists of:

- FastAPI API layer
- PostgreSQL persistence
- Redis + ARQ background job queue
- LangGraph workflow orchestration
- Repository analysis engine
- Implementation planning engine
- Code modification engine
- Pull request tracking
- Audit logging

Architecture source:

```text
docs/diagrams/adwe-architecture.mmd
```

## Local Development

Start infrastructure and API:

```bash
docker compose up --build
```

Health check:

```bash
curl http://localhost:8000/v1/health
```

Create a workflow:

```bash
curl -X POST http://localhost:8000/v1/workflows \
  -H "Content-Type: application/json" \
  -d '{"repository_url":"https://github.com/pallets/flask"}'
```

List workflows:

```bash
curl http://localhost:8000/v1/workflows
```

Metrics:

```bash
curl http://localhost:8000/metrics
```

## GitHub Authentication

For private repositories, create a GitHub Personal Access Token.

Create a local `.env` file:

```env
GITHUB_TOKEN=your_token_here
```

## Production Readiness

Current capabilities:

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
- Workflow execution timestamps
- Retry tracking
- Queue metrics
- Worker heartbeat monitoring

## End-to-End Demo

Start the stack:

```bash
docker compose up --build
```

Create a workflow:

```bash
curl -X POST http://localhost:8000/v1/workflows \
  -H "Content-Type: application/json" \
  -d '{"repository_url":"https://github.com/pallets/flask"}'
```

Inspect workflow:

```bash
curl http://localhost:8000/v1/workflows/<workflow_id>
```

Workflow summary:

```bash
curl http://localhost:8000/v1/workflows/<workflow_id>/summary
```

Workflow artifacts:

```bash
curl http://localhost:8000/v1/workflows/<workflow_id>/artifacts
```

Workflow metrics:

```bash
curl http://localhost:8000/v1/workflow-metrics
```

Queue metrics:

```bash
curl http://localhost:8000/v1/queue-metrics
```

## Pre-Push Checklist

```bash
PYTHONPATH=src uv run pytest
PYTHONPATH=src uv run alembic upgrade head
docker compose config
```

## Roadmap

Planned next features:

- Real GitHub branch creation
- Automatic patch application
- Git push automation
- Pull request creation
- OpenTelemetry tracing
- LLM-powered planning
- Role-based access control
- Production deployment manifests
