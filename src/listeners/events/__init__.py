from slack_bolt import App

from .sample_app_home import app_home_opened_callback
from .sample_app_mention import app_mention_callback

matcher_map = {
    "app_mention": app_mention_callback,
    "app_home_opened": app_home_opened_callback,
}


def register(app: App) -> None:
    """Register all event handlers with the given app.

    To add a new event, create a callback in this package and add it to matcher_map above.
    For the full list of available events and their payloads see https://api.slack.com/events.
    """
    for event_name, callback in matcher_map.items():
        app.event(event_name)(callback)
