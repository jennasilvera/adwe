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
