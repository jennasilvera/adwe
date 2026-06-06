from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator
from adwe.core.logging import configure_logging
from sqlalchemy import text

from adwe.api.workflows import router as workflows_router
from adwe.api.middleware import RequestIDMiddleware
from adwe.api.audit import router as audit_router
from adwe.api.patches import router as patches_router
from adwe.api.patch_apply import router as patch_apply_router
from adwe.db.session import engine

configure_logging()

app = FastAPI(title="Agentic Development Workflow Engine")

app.add_middleware(RequestIDMiddleware)
app.include_router(workflows_router)
app.include_router(audit_router)
app.include_router(patches_router)
app.include_router(patch_apply_router)

Instrumentator().instrument(app).expose(app)


@app.get("/v1/health")
async def health():
    async with engine.connect() as conn:
        await conn.execute(text("SELECT 1"))

    return {"status": "ok", "database": "ok"}
