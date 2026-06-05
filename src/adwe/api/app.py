from fastapi import FastAPI

app = FastAPI(title="Agentic Development Workflow Engine")

@app.get("/v1/health")
def health():
    return {"status": "ok"}
