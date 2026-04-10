from datarobot.core.config import DataRobotAppFrameworkBaseSettings


class Config(DataRobotAppFrameworkBaseSettings):
    """Application configuration.

    Reads variables from environment variables (including DataRobot Runtime Parameters),
    .env files, and file secrets — handled automatically by DataRobotAppFrameworkBaseSettings.

    Runtime Parameter names map directly to env var names (e.g. SLACK_BOT_TOKEN).
    """

    slack_bot_token: str | None = None
    slack_app_token: str | None = None
    # Full LiteLLM model string for the DataRobot LLM Gateway.
    # Find available models with: datarobot.genai.LLMGatewayCatalog().list_as_dict()
    # See: https://github.com/carsongee/get-datarobot-llms
    datarobot_llm_model: str = "azure/gpt-5-1-2025-11-13"
