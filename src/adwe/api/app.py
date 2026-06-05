from fastapi import FastAPI
from sqlalchemy import text

from adwe.api.workflows import router as workflows_router
from adwe.db.session import engine

app = FastAPI(title="Agentic Development Workflow Engine")

app.include_router(workflows_router)


@app.get("/v1/health")
async def health():
    async with engine.connect() as conn:
        await conn.execute(text("SELECT 1"))

    return {"status": "ok", "database": "ok"}
