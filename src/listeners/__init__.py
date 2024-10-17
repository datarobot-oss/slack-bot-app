from . import events
from . import messages

def register_listeners(app):
    events.register(app)
    messages.register(app)
