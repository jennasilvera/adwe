from fastapi import FastAPI
from sqlalchemy import text

from adwe.db.session import engine

app = FastAPI(title="Agentic Development Workflow Engine")


@app.get("/v1/health")
async def health():
    async with engine.connect() as conn:
        await conn.execute(text("SELECT 1"))

    return {"status": "ok", "database": "ok"}
