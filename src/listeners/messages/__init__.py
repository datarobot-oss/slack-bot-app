import re
from typing import Any

from slack_bolt import App, Say

from .sample_messages import goodbye_message_callback, potato_callback, welcome_message_callback


def register(app: App) -> None:
    """Register all message handlers with the given app.

    Message handlers trigger on plain channel/DM messages without an @mention.
    They require additional OAuth scopes (channels:history, im:history, im:read, im:write)
    and the corresponding Slack event subscriptions (message.channels, message.im).

    Use the ``@app.message`` decorator for simple string or regex matches:

    .. code-block:: python

        @app.message("Hello!")
        def hi(message: dict[str, Any], say: Say) -> None:
            say(f"Hi there <@{message['user']}>! :wave:")

    Or pass a compiled regex for case-insensitive / multi-word patterns:

    .. code-block:: python

        @app.message(re.compile(r"(hi|hey|hello)", re.IGNORECASE))
        def welcome(context, say, logger):
            greeting = context["matches"][0]
            say(f"{greeting}, how are you?")
    """
    # Enabled by default — responds to "potato" in any message.
    app.message(re.compile(r"potato", re.IGNORECASE))(potato_callback)

    # Uncomment the handlers below to respond to greetings and farewells.
    # These require the message.channels / message.im event subscriptions.
    # app.message(re.compile(r"(hi|hey|hello)", re.IGNORECASE))(welcome_message_callback)
    # app.message(re.compile(r"(goodbye|bye|farewell)", re.IGNORECASE))(goodbye_message_callback)
