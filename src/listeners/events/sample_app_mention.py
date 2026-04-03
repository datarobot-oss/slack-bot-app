from logging import Logger

from slack_bolt import Say


def app_mention_callback(event: dict, logger: Logger, say: Say) -> None:
    """Respond to @-mentions by echoing the user's message back to the channel."""
    user_id = event["user"]
    message_text = event["text"]
    logger.info("App mentioned by user %s: %s", user_id, message_text)
    say(f"Hi there, <@{user_id}>! You mentioned me with the text: {message_text}")
