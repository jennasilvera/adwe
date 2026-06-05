FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && \
    apt-get install -y git && \
    rm -rf /var/lib/apt/lists/*

COPY pyproject.toml uv.lock ./

RUN pip install uv && uv sync --frozen

COPY src ./src

ENV PYTHONPATH=src

CMD ["uv", "run", "uvicorn", "adwe.api.app:app", "--host", "0.0.0.0", "--port", "8000"]
