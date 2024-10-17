import logging
import os
import signal
import sys

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

from listeners import register_listeners

logger = logging.getLogger(__name__)

BOT_TOKEN = os.environ.get("slack_bot_token")
APP_TOKEN = os.environ.get("slack_app_token")

app_handler: SocketModeHandler | None = None

def initiate_app_handler():
    global app_handler
    slack_app = App(token=BOT_TOKEN)
    register_listeners(slack_app)
    app_handler = SocketModeHandler(slack_app, APP_TOKEN)

def handle_shutdown(signum, frame):
    app_handler.close()
    sys.exit(0)

if __name__ == "__main__":
    if BOT_TOKEN and APP_TOKEN:
        initiate_app_handler()

        signal.signal(signal.SIGTERM, handle_shutdown)
        signal.signal(signal.SIGINT, handle_shutdown)

        app_handler.start()
    else:
        sys.exit(0)
