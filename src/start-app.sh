#!/usr/bin/env bash
echo "Starting App"

export token="$DATAROBOT_API_TOKEN"
export endpoint="$DATAROBOT_ENDPOINT"

if [ -n "$MLOPS_RUNTIME_PARAM_SLACK_BOT_TOKEN" ]; then
  export slack_bot_token=$(echo "$MLOPS_RUNTIME_PARAM_SLACK_BOT_TOKEN" | grep -o '"apiToken":"[^"]*' | sed 's/"apiToken":"//')
else
  export slack_bot_token="$SLACK_BOT_TOKEN"
fi
if [ -n "$MLOPS_RUNTIME_PARAM_SLACK_APP_TOKEN" ]; then
  export slack_app_token=$(echo "$MLOPS_RUNTIME_PARAM_SLACK_APP_TOKEN"| grep -o '"apiToken":"[^"]*' | sed 's/"apiToken":"//')
else
  export slack_app_token="$SLACK_APP_TOKEN"
fi

gunicorn -b :8080 flask_app:flask_app  --timeout 200 --graceful-timeout 30 &

GUNICORN_PID=$!

python3 slack_app.py &

SLACK_APP_PID=$!

wait $GUNICORN_PID
wait $SLACK_APP_PID