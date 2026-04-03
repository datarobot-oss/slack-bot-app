# Slack bot app template

In this repository you will find a ready-to-use Slack bot template for a DataRobot Custom Application. After creating the Slack application, you can immediately start configuring the bot messages and events.

The Slack bot code is based on the [Bolt for Python starter template](https://github.com/slack-samples/bolt-python-starter-template/tree/main) and
comes with a small FastAPI app and start-app script to create a working DataRobot Custom Application.

## Setup

Follow the configuration outlined in the steps below.

### Create a new Slack app

> **Important:** This template requires a modern Slack app with Socket Mode support. Slack apps created before 2021 (legacy apps) do not support Socket Mode and cannot be used with this template. Always create a new app.

[Create a new Slack application](https://api.slack.com/apps?new_app=1) and select **From a manifest**. This is the recommended approach — the repository includes a [manifest.json](https://github.com/datarobot-oss/slack-bot-app/blob/main/manifest.json) that configures all required scopes, events, and settings in one step.

1. Select **From a manifest** and choose your workspace.
2. Select the **JSON** tab and paste the contents of [manifest.json](https://github.com/datarobot-oss/slack-bot-app/blob/main/manifest.json).
3. Update the app name in `display_information > name` and the bot display name in `features > bot_user > display_name`.
4. Review the permissions and confirm the app creation.

The manifest pre-configures all OAuth scopes and event subscriptions the bot needs. Adding scopes later requires reinstalling the app to your workspace — if your organisation requires IT approval for Slack app installs, plan your scope requirements upfront.

### Generate tokens

The bot requires two tokens. Generate them in the order below — **Socket Mode must be enabled before generating the App Token**, otherwise the required scope will not appear.

**Step 1 — Enable Socket Mode**

Go to **Settings → Socket Mode** and toggle it on. This makes the bot connect to Slack over a persistent WebSocket instead of requiring a public URL.

**Step 2 — Generate `SLACK_APP_TOKEN`**

Go to **Basic Information → App-Level Tokens** and click **Generate Token and Scopes**. Add the `connections:write` scope — this is the only scope that allows the bot to open a WebSocket connection. Copy the generated token (it starts with `xapp-`).

> If you only see `authorizations:read` and `app_configurations:write` as scope options, Socket Mode is not enabled yet. Go back to Step 1.

**Step 3 — Generate `SLACK_BOT_TOKEN`**

Go to **OAuth & Permissions** and click **Install to workspace**. Review the permissions and confirm. Once installed, copy the **Bot User OAuth Token** from the same page (it starts with `xoxb-`).

> Adding or changing OAuth scopes after installation requires a reinstall. Go to **OAuth & Permissions → Reinstall to workspace** after any scope changes.

### Run the app

You can run the bot inside DataRobot using a Custom Application or by running the app locally. Custom Applications can be created via the Registry's **Applications** page or by using [DRApps](https://github.com/datarobot/dr-apps/blob/main/README.md).

Define the variables for the app to communicate with Slack. If you run the app locally or via another environment, then you need to set the environment variables in the terminal that you use. When this app is run via the **Applications** page, the variables can be set with the preconfigured runtime parameters in the application source.

**For a local run:**

```shell
cd src
uv sync
export SLACK_APP_TOKEN="xapp-..."
export SLACK_BOT_TOKEN="xoxb-..."
./start-app.sh
```

**For the Applications page:**

Use `[DataRobot] Python 3.12` as the base environment and set the tokens in the runtime parameters section. To do that,
click the edit icon, expand the value dropdown, and select **Add credentials**. Follow the instructions to add the tokens as `API Tokens` and return to the application source. Now select the newly created credentials to the corresponding variable.
Lastly, scroll to the top of the application source and click **Build application**.

### Test the bot

The bot responds to @mentions only. Invite it to a channel with `/invite @your-bot-name`, then try the following:

- `@your-bot-name ask what is the capital of France?` — the bot will answer via the DataRobot LLM Gateway
- `@your-bot-name help` — the bot will list available commands
- `@your-bot-name Hello!` — the bot will echo your message back
- Open the bot's **App Home** tab to see an overview of available commands

### DataRobot LLM Gateway

The bot includes an `@mention ask <question>` command powered by the [DataRobot LLM Gateway](https://docs.datarobot.com/en/docs/gen-ai/genai-code/dr-llm-gateway.html). It uses the application's own `DATAROBOT_API_TOKEN` (injected automatically by the platform) so no additional configuration is required to get started.

To use a different model, set the `DATAROBOT_LLM_MODEL` environment variable to any `model` value from `GET /api/v2/genai/llmgw/catalog/` (e.g. `azure-openai-gpt-4-o`). The default is `azure-openai-gpt-4-o-mini`.

Optionally, set `DATAROBOT_USER_API_TOKEN` via runtime parameters to use your personal DataRobot API token instead of the application-scoped one.

### Disable auto-stopping

Custom applications auto-stop after a while of inactivity. To turn this off for your Slack bot, please run the following
command using your `<application_id>` and `<authorization_token>`:

```shell
curl --location --request PATCH 'https://app.datarobot.com/api/v2/customApplications/<application_id>/' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer <authorization_token>' \
--data '{
    "allowAutoStopping": false
}'
```

## Troubleshooting

**The bot connects but does not respond to @mentions**

Make sure the `app_mention` event is subscribed under **Event Subscriptions → Subscribe to bot events**. Socket Mode still requires explicit event subscriptions — it only changes how events are delivered (WebSocket instead of HTTP), not which events are sent. Invite the bot to the channel with `/invite @your-bot-name` if you have not already done so.

**The bot does not respond to plain messages (`hi`, `potato`, etc.)**

Plain message handlers are disabled by default. Enable them by adding entries to `matcher_map` in [src/listeners/messages/\_\_init\_\_.py](src/listeners/messages/__init__.py). These handlers also require additional OAuth scopes (`channels:history`, `im:history`, `im:read`, `im:write`) and event subscriptions (`message.channels`, `message.im`) — all of which are already included in the manifest. If your organisation requires IT approval for these scopes, the @mention-only mode works without them.

**`connections:write` scope is not available when generating the App Token**

Socket Mode is not enabled. Go to **Settings → Socket Mode**, enable it, and then return to **Basic Information → App-Level Tokens** to generate the token.

**`missing_scope: chat:write` error in the logs**

The bot token was generated before `chat:write` was added to the app's scopes, or the app was created without the manifest. Go to **OAuth & Permissions → Reinstall to workspace** to apply the current scope configuration.

**`missing_scope: connections:write` / `provided: app_configurations:write` error**

The App Token was generated with the wrong scope. Delete it from **Basic Information → App-Level Tokens** and generate a new one with `connections:write`.

**Event subscriptions page shows a "Request URL" field and Save is disabled**

This happens when Socket Mode is not enabled — the page falls back to HTTP mode and requires a verified URL before saving. Enable Socket Mode first (**Settings → Socket Mode**), then return to configure event subscriptions.

## Add more actions

You can find examples for all available Slack listeners in the [Bolt for Python starter template](https://github.com/slack-samples/bolt-python-starter-template/tree/main). The approach is the exact same as in this repository, but they provide other, more advanced actions.
This workflow only focuses on how to add more message and event listeners. Note that some events might require additional scopes and permissions. These are all mentioned within the events list on `https://api.slack.com/events`. To add new scopes to an existing app, go to the Slack **OAuth & Permissions** page and find the **Scopes** section. Once you add new scope to the app it might require to be reinstalled.

### Events

To configure events, navigate to `src/listeners/events` and create a new file that contains the function you would like to run as callback to an event. You can use the sample app mention as an example:

```python
from logging import Logger
from slack_bolt import Say

def app_mention_callback(event: dict, logger: Logger, say: Say) -> None:
    user_id = event["user"]
    message_text = event["text"]
    logger.info("App mentioned by user %s: %s", user_id, message_text)
    say(f"Hi there, <@{user_id}>! You mentioned me with the text: {message_text}")
```

Once you have defined a callback function, it needs to be registered to the right event.
Navigate to the `__init__.py` in `events` and add the event name with the callback to the `matcher_map`:

```python
matcher_map = {
    "app_mention": app_mention_callback,
    # Add more events and callbacks here
}
```

### Messages

Messages are registered almost the same way as events. Navigate to `src/listeners/messages` and create a new file that contains the function you would like to run as callback. Here is a sample callback:

```python
from logging import Logger
from slack_bolt import BoltContext, Say

def goodbye_message_callback(context: BoltContext, say: Say, logger: Logger) -> None:
    farewell = context["matches"][0]
    logger.info("Responding to farewell: %s", farewell)
    say(f"{farewell}, see you next time!")
```

Once you have defined a callback function, it needs to be registered to the right text matcher.
Navigate to the `__init__.py` in `messages` and add the string that should trigger the callback to the matcher_map:

```python
matcher_map = {
    r"(hi|hey|hello)": welcome_message_callback,
    r"(goodbye|bye|farewell)": goodbye_message_callback,
    r"help": help_message_callback,
}
```

Be aware that unrelated conversations could trigger the bot if the matching phrase is too common! As a default this
bot template will ignore upper and lower case to avoid issues between `Hi` and `hi`. If you need the matcher to react
differently between upper and lower case, edit the `register` function by removing `re.IGNORECASE` from
`app.message(re.compile(pattern, re.IGNORECASE))(callback)`
