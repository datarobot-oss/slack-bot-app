from logging import Logger

from slack_bolt import App
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

from .sample_app_mention import app_mention_callback


def register(app: App) -> None:
    """Register all event handlers with the given app.

    To add a new event handler, either define a function and decorate it with
    ``@app.event("<event_name>")`` directly here, or create a callback in its
    own module and register it with ``app.event("<event_name>")(callback)``.

    For the full list of available events see https://api.slack.com/events.
    """
    app.event("app_mention")(app_mention_callback)

    @app.event("app_home_opened")
    def app_home_opened(client: WebClient, event: dict, logger: Logger) -> None:
        """Publish the App Home tab when a user opens it."""
        user_id = event["user"]
        try:
            client.views_publish(
                user_id=user_id,
                view={
                    "type": "home",
                    "blocks": [
                        {
                            "type": "header",
                            "text": {"type": "plain_text", "text": "Slack Bot Template"},
                        },
                        {
                            "type": "section",
                            "text": {
                                "type": "mrkdwn",
                                "text": (
                                    "Interact with this bot by @mentioning it:\n\n"
                                    "• *@mention ask <question>* — answer via the DataRobot LLM Gateway\n"
                                    "• *@mention summarize* or *@mention summarize last N* — summarize recent channel messages\n"
                                    "• *@mention help* — list available commands\n"
                                    "• *@mention <anything else>* — echo it back"
                                ),
                            },
                        },
                    ],
                },
            )
        except SlackApiError:
            logger.exception("Failed to publish App Home for user %s", user_id)
