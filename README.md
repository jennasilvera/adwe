
## Local Development

Start infrastructure and API:

```bash
docker compose up --build
curl http://localhost:8000/v1/health
curl -X POST http://localhost:8000/v1/workflows \
  -H "Content-Type: application/json" \
  -d '{"repository_url":"https://github.com/jennasilvera/adwe"}'
curl -X POST http://localhost:8000/v1/workflows/<workflow_id>/run
curl http://localhost:8000/v1/workflows
curl http://localhost:8000/metrics
cat >> README.md <<'EOF'

## Local Development

Start infrastructure and API:

```bash
docker compose up --build
