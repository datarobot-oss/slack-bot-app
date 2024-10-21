from slack_bolt import App

from .sample_app_mention import app_mention_callback

matcher_map = {
    "app_mention": app_mention_callback,
}

def register(app: App):
    # Register multiple event handlers, add additional event types in the matcher_map above
    # See the full event list and their payload on https://api.slack.com/events
    for event_name, callback in matcher_map.items():
        app.event(event_name)(callback)
