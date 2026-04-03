import os

from openai import OpenAI

_DATAROBOT_ENDPOINT = os.environ.get("DATAROBOT_ENDPOINT", "https://app.datarobot.com/api/v2")

# Prefer the user-supplied token (runtime parameter) over the app-scoped token.
# The app token works for /genai/llmgw/ but may have different quotas/access than the user's own token.
_DATAROBOT_API_TOKEN = os.environ.get("DATAROBOT_USER_API_TOKEN") or os.environ.get("DATAROBOT_API_TOKEN")

# Model to use for LLM Gateway requests.
# Must be prefixed with "datarobot/" — e.g. "datarobot/azure/gpt-4o-mini".
# List available models via GET /api/v2/genai/llmgw/catalog/
DATAROBOT_LLM_MODEL = os.environ.get("DATAROBOT_LLM_MODEL", "datarobot/azure/gpt-4o-mini")


def get_llm_client() -> OpenAI:
    """Return an OpenAI-compatible client pointed at the DataRobot LLM Gateway.

    Uses DATAROBOT_USER_API_TOKEN if provided (set via runtime parameters),
    falling back to the platform-injected DATAROBOT_API_TOKEN.
    """
    return OpenAI(
        api_key=_DATAROBOT_API_TOKEN,
        base_url=_DATAROBOT_ENDPOINT.rstrip("/") + "/genai/llmgw",
    )
