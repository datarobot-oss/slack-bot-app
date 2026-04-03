import os
from pathlib import Path

from openai import OpenAI

_DATAROBOT_ENDPOINT = os.environ.get("DATAROBOT_ENDPOINT", "https://app.datarobot.com/api/v2")

# Prefer the user-supplied token (runtime parameter) over the app-scoped token.
# The app token works for /genai/llmgw/ but may have different quotas/access than the user's own token.
_DATAROBOT_API_TOKEN = os.environ.get("DATAROBOT_USER_API_TOKEN") or os.environ.get("DATAROBOT_API_TOKEN")

# Model to use for LLM Gateway requests.
# Use the model field from GET /api/v2/genai/llmgw/catalog/ — e.g. "azure-openai-gpt-4-o-mini".
DATAROBOT_LLM_MODEL = os.environ.get("DATAROBOT_LLM_MODEL", "azure-openai-gpt-4-o-mini")

# System prompt loaded from skills.md — controls tone, formatting, and behaviour.
SYSTEM_PROMPT = (Path(__file__).parent / "skills.md").read_text()


def get_llm_client() -> OpenAI:
    """Return an OpenAI-compatible client pointed at the DataRobot LLM Gateway.

    Uses DATAROBOT_USER_API_TOKEN if provided (set via runtime parameters),
    falling back to the platform-injected DATAROBOT_API_TOKEN.
    """
    return OpenAI(
        api_key=_DATAROBOT_API_TOKEN,
        base_url=_DATAROBOT_ENDPOINT.rstrip("/") + "/genai/llmgw",
    )
