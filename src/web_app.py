import os

from fastapi import FastAPI

app = FastAPI()

BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN")
APP_TOKEN = os.environ.get("SLACK_APP_TOKEN")


@app.get("/")
async def root() -> dict:
    """Return bot configuration status."""
    return {
        "name": "Slack Bot Template",
        "status": "running" if (BOT_TOKEN and APP_TOKEN) else "degraded",
        "tokens": {
            "SLACK_BOT_TOKEN": "configured" if BOT_TOKEN else "missing",
            "SLACK_APP_TOKEN": "configured" if APP_TOKEN else "missing",
        },
    }


@app.get("/healthz")
async def healthz() -> dict:
    """Liveness probe endpoint."""
    return {"status": "ok"}
