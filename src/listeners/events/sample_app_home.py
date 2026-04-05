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
    except Exception:
        logger.exception("Failed to publish App Home for user %s", user_id)
