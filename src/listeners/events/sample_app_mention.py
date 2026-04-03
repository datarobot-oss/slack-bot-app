import re
from logging import Logger

from slack_bolt import Say

from datarobot_client import DATAROBOT_LLM_MODEL, get_llm_client

_MENTION_RE = re.compile(r"<@[A-Z0-9]+>\s*", re.IGNORECASE)


def app_mention_callback(event: dict, logger: Logger, say: Say) -> None:
    """Route @mention messages to the appropriate handler.

    Supported commands (all prefixed with @mention):
      ask <question>  — answer via the DataRobot LLM Gateway
      help            — list available commands
      <anything else> — echo the message back
    """
    user_id = event["user"]
    text = _MENTION_RE.sub("", event["text"]).strip()

    ask_match = re.match(r"ask\s+(.+)", text, re.IGNORECASE)
    if ask_match:
        question = ask_match.group(1).strip()
        logger.info("LLM Gateway request from %s: %s", user_id, question)
        try:
            response = get_llm_client().chat.completions.create(
                model=DATAROBOT_LLM_MODEL,
                messages=[{"role": "user", "content": question}],
            )
            say(response.choices[0].message.content)
        except Exception:
            logger.exception("LLM Gateway request failed")
            say("Sorry, I couldn't get a response. Please check the bot logs or try again later.")
    elif re.match(r"help", text, re.IGNORECASE):
        say(
            "Here's what I can do (prefix every command with @mention):\n"
            "• *ask <question>* — I'll answer via the DataRobot LLM Gateway\n"
            "• *help* — I'll show this message\n"
            "• *anything else* — I'll echo it back"
        )
    else:
        logger.info("App mentioned by user %s: %s", user_id, text)
        say(f"Hi there, <@{user_id}>! You mentioned me with: {text}")
