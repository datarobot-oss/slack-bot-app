import logging
import os
import signal
import sys
import threading

import uvicorn
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

from listeners import register_listeners
from web_app import app as web_app

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN")
SLACK_APP_TOKEN = os.environ.get("SLACK_APP_TOKEN")

app_handler: SocketModeHandler | None = None


def create_app_handler() -> SocketModeHandler:
    """Initialise the Slack Bolt app and return a ready-to-start SocketModeHandler."""
    slack_app = App(token=SLACK_BOT_TOKEN)
    register_listeners(slack_app)
    return SocketModeHandler(slack_app, SLACK_APP_TOKEN)


def handle_shutdown(_signum, _frame) -> None:
    """Gracefully close the Slack socket connection on SIGTERM/SIGINT."""
    if app_handler:
        app_handler.close()
    sys.exit(0)


if __name__ == "__main__":
    threading.Thread(
        target=lambda: uvicorn.run(web_app, host="0.0.0.0", port=8080, log_level="warning"),
        daemon=True,
    ).start()

    signal.signal(signal.SIGTERM, handle_shutdown)
    signal.signal(signal.SIGINT, handle_shutdown)

    if not SLACK_BOT_TOKEN:
        logger.error("Missing required environment variable: SLACK_BOT_TOKEN")
    if not SLACK_APP_TOKEN:
        logger.error("Missing required environment variable: SLACK_APP_TOKEN")

    if SLACK_BOT_TOKEN and SLACK_APP_TOKEN:
        app_handler = create_app_handler()
        app_handler.start()
    else:
        # Keep the process alive so the FastAPI health endpoint remains reachable
        # while the operator resolves the missing token configuration.
        threading.Event().wait()
