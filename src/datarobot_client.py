from pathlib import Path

import datarobot
import litellm

# System prompt loaded from system_prompt.md — controls tone, formatting, and behaviour.
SYSTEM_PROMPT = (Path(__file__).parent / "system_prompt.md").read_text()


def ask_llm(model: str, question: str) -> str:
    """Send a question to the DataRobot LLM Gateway via LiteLLM and return the response text.

    Uses datarobot.Client() to resolve the API token and endpoint, supporting all
    credential sources (env vars, .env files, Runtime Parameters, etc.).

    Discover available models with::

        import datarobot
        catalog = datarobot.genai.LLMGatewayCatalog()
        print(catalog.list_as_dict())

    See also: https://github.com/carsongee/get-datarobot-llms
    """
    dr = datarobot.Client()
    # LiteLLM requires the "datarobot/" prefix to route through the DR LLM Gateway.
    # Accept both "datarobot/azure/gpt-4o" and the short form "azure/gpt-4o".
    if not model.startswith("datarobot/"):
        model = f"datarobot/{model}"
    response = litellm.completion(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": question},
        ],
        api_key=dr.token,
        api_base=dr.endpoint,
    )
    return response.choices[0].message.content
