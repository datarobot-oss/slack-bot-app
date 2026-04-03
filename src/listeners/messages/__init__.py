import re

from slack_bolt import App

from .sample_messages import potato_callback

# Message handlers trigger on plain channel/DM messages without an @mention.
# They require additional OAuth scopes (channels:history, im:history, im:read, im:write)
# and the corresponding Slack event subscriptions (message.channels, message.im).
# If your app has those scopes, uncomment the entries below or add your own —
# see sample_messages.py and sample_llm.py for ready-to-use examples.
matcher_map: dict = {
    # r"(hi|hey|hello)": welcome_message_callback,
    # r"(goodbye|bye|farewell)": goodbye_message_callback,
    # r"help": help_message_callback,
    r"potato": potato_callback,
}


def register(app: App) -> None:
    """Register all message handlers with the given app.

    To add a new handler, create a callback in this package and add a regex pattern
    pointing to it in matcher_map above. Patterns are matched case-insensitively by default.
    Note: overly broad patterns may trigger the bot on unrelated conversations.
    """
    for pattern, callback in matcher_map.items():
        app.message(re.compile(pattern, re.IGNORECASE))(callback)
