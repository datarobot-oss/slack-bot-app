from logging import Logger

from slack_sdk import WebClient


def app_home_opened_callback(client: WebClient, event: dict, logger: Logger) -> None:
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
                                "Here's what this bot can do:\n\n"
                                "• *@mention the bot* — it will echo your message\n"
                                "• Say *hi*, *hey*, or *hello* — it will greet you\n"
                                "• Say *goodbye*, *bye*, or *farewell* — it will say farewell\n"
                                "• Say *ask <question>* — it will answer via the DataRobot LLM Gateway\n"
                                "• Say *help* — it will list these commands"
                            ),
                        },
                    },
                ],
            },
        )
    except Exception:
        logger.exception("Failed to publish App Home for user %s", user_id)
