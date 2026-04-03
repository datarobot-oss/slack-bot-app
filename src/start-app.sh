#!/usr/bin/env bash
export DATAROBOT_LLM_MODEL="vertex_ai/claude-sonnet-4-6"

echo "Starting App"

if [ -n "$MLOPS_RUNTIME_PARAM_SLACK_BOT_TOKEN" ]; then
  export SLACK_BOT_TOKEN=$(echo "$MLOPS_RUNTIME_PARAM_SLACK_BOT_TOKEN" | grep -o '"apiToken":"[^"]*' | sed 's/"apiToken":"//')
else
  export SLACK_BOT_TOKEN="$SLACK_BOT_TOKEN"
fi
if [ -n "$MLOPS_RUNTIME_PARAM_SLACK_APP_TOKEN" ]; then
  export SLACK_APP_TOKEN=$(echo "$MLOPS_RUNTIME_PARAM_SLACK_APP_TOKEN" | grep -o '"apiToken":"[^"]*' | sed 's/"apiToken":"//')
else
  export SLACK_APP_TOKEN="$SLACK_APP_TOKEN"
fi
if [ -n "$MLOPS_RUNTIME_PARAM_DATAROBOT_USER_API_TOKEN" ]; then
  export DATAROBOT_USER_API_TOKEN=$(echo "$MLOPS_RUNTIME_PARAM_DATAROBOT_USER_API_TOKEN" | grep -o '"apiToken":"[^"]*' | sed 's/"apiToken":"//')
else
  export DATAROBOT_USER_API_TOKEN="$DATAROBOT_USER_API_TOKEN"
fi

exec python3 slack_app.py
