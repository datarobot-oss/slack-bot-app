import logging
import os

from flask import Flask, render_template
from werkzeug.middleware.proxy_fix import ProxyFix

logger = logging.getLogger(__name__)

base_dir = os.path.abspath(os.path.dirname(__file__))
flask_app = Flask(__name__, template_folder=os.path.join(base_dir, 'templates'))
flask_app.wsgi_app = ProxyFix(flask_app.wsgi_app, x_prefix=1)

BOT_TOKEN = os.environ.get("slack_bot_token")
APP_TOKEN = os.environ.get("slack_app_token")

@flask_app.route("/")
def index_health():
    if BOT_TOKEN and APP_TOKEN:
        return render_template("index.html", message="Slack bot is running!", success=True)
    else:
        logger.error("Missing required Slack App and/or Bot tokens!")
        has_bot_token = True if BOT_TOKEN else False
        has_app_token = True if APP_TOKEN else False
        return render_template("index.html",
                               message="Slack bot is not running!",
                               success=False,
                               has_bot_token=has_bot_token,
                               has_app_token=has_app_token)

if __name__ == "__main__":
    flask_app.run(host="0.0.0.0", debug=False, port=8080)
