import re
from logging import Logger

from slack_bolt import Say
from slack_sdk import WebClient

from config import Config
from datarobot_client import ask_llm

_MENTION_RE = re.compile(r"<@[A-Z0-9]+>\s*", re.IGNORECASE)
_SUMMARIZE_RE = re.compile(r"summarize\b(?:\s+(?:last\s+)?(\d+))?", re.IGNORECASE)

_DEFAULT_SUMMARY_MESSAGES = 20
_MAX_SUMMARY_MESSAGES = 100


def _build_transcript(client: WebClient, channel: str, limit: int) -> str:
    """Fetch channel history and return a chronological transcript string.

    The most recent message (the triggering mention) is excluded.
    User IDs are resolved to display names where possible.
    """
    result = client.conversations_history(channel=channel, limit=limit + 1)
    messages = result.get("messages", [])

    # Drop the triggering mention — it is always the first (newest) entry
    if messages:
        messages = messages[1:]

    # Oldest first
    messages = list(reversed(messages))

    user_cache: dict[str, str] = {}

    def resolve(user_id: str) -> str:
        if user_id not in user_cache:
            try:
                info = client.users_info(user=user_id)
                user = info["user"]
                profile = user.get("profile", {})
                user_cache[user_id] = profile.get("display_name") or profile.get("real_name") or user_id
            except Exception:
                user_cache[user_id] = user_id
        return user_cache[user_id]

    lines = []
    for msg in messages:
        if msg.get("subtype"):
            continue  # skip join/leave/bot notices
        name = resolve(msg["user"]) if "user" in msg else "bot"
        lines.append(f"{name}: {msg.get('text', '')}")

    return "\n".join(lines)


def _ask_llm(question: str, logger: Logger, say: Say) -> None:
    """Send a question to the LLM Gateway and reply with the answer."""
    logger.info("LLM Gateway request: %s", question)
    try:
        model = Config().datarobot_llm_model
        say(ask_llm(model, question))
    except Exception:
        logger.exception("LLM Gateway request failed")
        say("Sorry, I couldn't get a response. Please check the bot logs or try again later.")


def app_mention_callback(event: dict, client: WebClient, logger: Logger, say: Say) -> None:
    """Route @mention messages to the appropriate handler.

    Supported commands (all prefixed with @mention):
      ask <question>          — answer via the DataRobot LLM Gateway
      summarize [last N]      — summarize the last N channel messages (default 20, max 100)
                                requires the channels:history OAuth scope
      help                    — list available commands
      <anything else>         — echo the message back
    """
    user_id = event["user"]
    text = _MENTION_RE.sub("", event["text"], count=1).strip()

    ask_match = re.match(r"ask\s+(.+)", text, re.IGNORECASE | re.DOTALL)
    summarize_match = re.match(_SUMMARIZE_RE, text)

    if ask_match:
        _ask_llm(ask_match.group(1).strip(), logger, say)

    elif summarize_match:
        raw = summarize_match.group(1)
        limit = min(int(raw) if raw else _DEFAULT_SUMMARY_MESSAGES, _MAX_SUMMARY_MESSAGES)
        logger.info("Summarize request from %s: last %d messages", user_id, limit)
        try:
            transcript = _build_transcript(client, event["channel"], limit)
        except Exception:
            logger.exception("Failed to fetch channel history")
            say("Sorry, I couldn't read the channel history. Make sure the `channels:history` scope is granted.")
            return
        if not transcript:
            say("There are no messages to summarize yet.")
            return
        _ask_llm(f"Summarize the following Slack conversation:\n\n{transcript}", logger, say)

    elif re.match(r"help\b", text, re.IGNORECASE):
        say(
            "Here's what I can do (prefix every command with @mention):\n"
            "• *ask <question>* — I'll answer via the DataRobot LLM Gateway\n"
            "• *summarize* or *summarize last N* — I'll summarize the last N messages in this channel\n"
            "• *help* — I'll show this message\n"
            "• *anything else* — I'll echo it back"
        )

    else:
        logger.info("App mentioned by user %s: %s", user_id, text)
        say(f"Hi there, <@{user_id}>! You mentioned me with: {text}")
