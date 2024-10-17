import re

from slack_bolt import App
from .sample_messages import welcome_message_callback, goodbye_message_callback

matcher_map = {
    r'(hi|hey|hello)': welcome_message_callback,
    r'(goodbye|bye|farewell)': goodbye_message_callback,
}

# To receive messages from a channel or dm your app must be a member!
def register(app: App):
    # Register multiple message handlers, add additional phrases and callbacks in the matcher_map above
    for pattern, callback in matcher_map.items():
        app.message(re.compile(pattern, re.IGNORECASE))(callback)