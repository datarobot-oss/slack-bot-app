from logging import Logger
from slack_bolt import Say

# Type for 'event' can be found in https://api.slack.com/events as it depends on which was triggered
def app_mention_callback(event, logger: Logger, say: Say = None):
    # Get the message text and user who mentioned the bot
    user_id = event["user"]
    message_text = event["text"]

    # Log the event
    logger.info(f"App mentioned by user {user_id}: {message_text}")

    # Respond to the user in the channel
    say(f"Hi there, <@{user_id}>! You mentioned me with the text: {message_text}")