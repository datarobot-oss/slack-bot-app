from slack_bolt import App

from . import events, messages


def register_listeners(app: App) -> None:
    """Register all Slack event and message listeners with the given app."""
    events.register(app)
    messages.register(app)
