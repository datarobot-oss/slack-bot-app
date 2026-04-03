from logging import Logger

from slack_bolt import BoltContext, Say

from datarobot_client import DATAROBOT_LLM_MODEL, get_llm_client


def ask_callback(context: BoltContext, say: Say, logger: Logger) -> None:
    """Send the user's question to the DataRobot LLM Gateway and reply with the answer.

    Triggered by messages matching: ask <question>
    The captured question is available as context["matches"][0].
    """
    question = context["matches"][0].strip()
    logger.info("LLM Gateway request: %s", question)

    try:
        client = get_llm_client()
        response = client.chat.completions.create(
            model=DATAROBOT_LLM_MODEL,
            messages=[{"role": "user", "content": question}],
        )
        answer = response.choices[0].message.content
        say(answer)
    except Exception:
        logger.exception("LLM Gateway request failed")
        say("Sorry, I couldn't get a response. Please check the bot logs or try again later.")
