from logging import Logger

from slack_bolt import BoltContext, Say


def welcome_message_callback(context: BoltContext, say: Say, logger: Logger) -> None:
    """Respond to greeting messages (hi / hey / hello) with a friendly reply."""
    greeting = context["matches"][0]
    logger.info("Responding to greeting: %s", greeting)
    say(f"{greeting}, how are you?")


def goodbye_message_callback(context: BoltContext, say: Say, logger: Logger) -> None:
    """Respond to farewell messages (goodbye / bye / farewell) with a parting reply."""
    farewell = context["matches"][0]
    logger.info("Responding to farewell: %s", farewell)
    say(f"{farewell}, see you next time!")


def potato_callback(say: Say) -> None:
    """Example message handler — replace this with your own logic."""
    say("Did someone say potato? :potato:")


