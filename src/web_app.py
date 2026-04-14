from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from config import Config
from datarobot_asgi_middleware import DataRobotASGIMiddleware

_templates = Jinja2Templates(directory=str(Path(__file__).parent / "templates"))

app = FastAPI()
app.add_middleware(DataRobotASGIMiddleware, health_endpoint="/healthz")


@app.get("/", response_class=HTMLResponse)
async def root(request: Request) -> HTMLResponse:
    """Human-readable status page."""
    config = Config()
    healthy = bool(config.slack_bot_token and config.slack_app_token)
    return _templates.TemplateResponse(
        request,
        "index.html",
        {
            "status_badge": "ok" if healthy else "err",
            "status_label": "Bot is running" if healthy else "Bot is not running",
            "bot_cls": "ok" if config.slack_bot_token else "err",
            "bot_val": "configured" if config.slack_bot_token else "missing",
            "app_cls": "ok" if config.slack_app_token else "err",
            "app_val": "configured" if config.slack_app_token else "missing",
            "llm_model": config.datarobot_llm_model,
        },
    )


@app.get("/healthz")
async def healthz() -> dict:
    """Liveness probe endpoint."""
    return {"status": "ok"}
