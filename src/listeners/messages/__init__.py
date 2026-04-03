import re

from slack_bolt import App

from .sample_llm import ask_callback
from .sample_messages import goodbye_message_callback, help_message_callback, welcome_message_callback

matcher_map = {
    r"(hi|hey|hello)": welcome_message_callback,
    r"(goodbye|bye|farewell)": goodbye_message_callback,
    r"help": help_message_callback,
    r"ask\s+(.+)": ask_callback,
}


def register(app: App) -> None:
    """Register all message handlers with the given app.

    To add a new handler, create a callback in this package and add a regex pattern
    pointing to it in matcher_map above. Patterns are matched case-insensitively by default.
    Note: overly broad patterns may trigger the bot on unrelated conversations.
    """
    for pattern, callback in matcher_map.items():
        app.message(re.compile(pattern, re.IGNORECASE))(callback)
