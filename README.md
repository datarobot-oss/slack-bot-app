# Slack bot app template

## What's in this repository?

In this repository you will find a ready-to-use Slack bot template for a DataRobot custom application.
After creating the Slack application, you can immediately start configuring the bot messages and events.

The Slack bot code is based on
the [Bolt for Python starter template](https://github.com/slack-samples/bolt-python-starter-template/tree/main) and
comes with a small Flask app and start-app script to create a working DataRobot custom application.

## How do I set it up?

### 1. Create a new Slack app

You need to create a new Slack application via the [Slack UI](https://api.slack.com/apps?new_app=1). Select either
`From scratch` or `From a manifest`, if you have never set up an app before we recommend using `From a manifest`.

The repository includes a basic [manifest.json](https://github.com/datarobot-oss/slack-bot-app/blob/main/manifest.json)
that you can copy & paste into the create app form. To set the app name, modify the `display_information > name`
and for the bot name `features > bot_user > display_name` or go to the `Basic Information` settings page after the
application has been created. Other information, such as the app icon, color or description can also be found in this
page.

Next select the workspace that the app should be installed to and afterward paste the manifest into the text field.
Make sure to select the JSON tab if you copied
the [manifest.json](https://github.com/datarobot-oss/slack-bot-app/blob/main/manifest.json)
from this repository.

On the last step it asks to review the permissions given to the bot. The manifest from this repository allows for
@-mentions
and messages, meaning it has access to the chat history of public channels it is a member of.

#### Short summary:

- [Create new app](https://api.slack.com/apps?new_app=1) from a manifest
- Select the workspace for the app
- Select `JSON` tab and paste
  the [manifest.json](https://github.com/datarobot-oss/slack-bot-app/blob/main/manifest.json)
  (modify the app name `display_information > name` and bot name `features > bot_user > display_name`)
- Review the given permissions
- Confirm the app creation

### 2. Generate the necessary tokens

**SLACK_APP_TOKEN**\
On the `Basic Information` page, scroll to find the `App-Level Tokens` section. Click the button to generate a
new token. Enter a name for the app token and add scope for `connections:write`, this will allow the app events over
WebSockets. Click generate and note down the token to be used as `SLACK_APP_TOKEN`.

**SLACK_BOT_TOKEN**\
The bot token can be found on the `OAuth & Permissions` page in `OAuth Tokens` section, here you will first need to
install the app to your selected Slack workspace. In the OAuth Tokens section click install to `{your workspace}` and
review the permissions. Once the app is installed note down the displayed token as `SLACK_BOT_TOKEN`.

#### Short summary:

- Generate the SLACK_APP_TOKEN:
  - On `Basic Information` page find `App-Level Tokens`
  - Click button to generate a new token
  - Enter token name and add scope for `connections:write`
  - Click generate and copy the token
- Generate the SLACK_BOT_TOKEN:
  - On `OAuth & Permissions` page find `App-Level Tokens` section
  - Install the app to your workspace
  - Copy the OAuth token

### 3. Run the app

You can run the Q&amp;A app in DataRobot using a custom application or by running the app locally.
Custom applications can be created via the Registry's Apps workshop or by
using [DRApps](https://github.com/datarobot/dr-apps/blob/main/README.md).

Define the variables for the app to communicate with Slack. If you run the app locally or via another environment,
then you'll need to set the env variables in the terminal that you use. When this app is run via
the **Applications** page, the variables can be set via the preconfigured runtime parameters in the application source.

**For local run:**
```shell
cd src
export SLACK_APP_TOKEN="xapp-..."
export SLACK_BOT_TOKEN="xoxb-..."
./start-app.sh
```
\
**For Apps workshop:**\
Use `[DataRobot] Python 3.12` as base environment and set the tokens in the runtime parameters section. To do that,
click
the edit pen, expand the value dropdown and select `Add credentials`. Follow the instructions to add the tokens as
`API Tokens`
and return to the application source. Now select the newly created credentials to the corresponding variable.
Finally scroll to the top of the application source and click `Build application`

### 4. Test the bot

Head over to your Slack chat and check it out using @-mention: `@testbot Hello!`. Be sure to use your own bot username
and to invite them to the public channel that you're testing within.
If the @-mention worked, you can also verify the messages sample by saying `hello` or `bye`

## How do I add more actions?

You can find examples for all available Slack listeners in the
[Bolt for Python starter template](https://github.com/slack-samples/bolt-python-starter-template/tree/main).
The approach is the exact same as in this repository, but they provide other, more advanced actions.

For this guide we will only focus on how to add more message and event listeners. Please note that some events might
require additional scopes and permissions. These are all mentioned within the events list
on https://api.slack.com/events.
To add new scopes to an existing app, go to the Slack `OAuth & Permissions` page and find the `Scopes` section.
Once you add new scope to the app it might require to be reinstalled.

### Events

For events navigate to `src/listeners/events` and create a new file that contains the function you would like to run
as callback to an event. We can use the sample app mention as example:

```python
def app_mention_callback(event, logger, say):
  # Get the message text and user who mentioned the bot
  user_id = event["user"]
  message_text = event["text"]

  # Respond to the user in the channel
  say(f"Hi there, <@{user_id}>! You mentioned me with the text: {message_text}")
```

Once you have defined a callback function, it needs to be registered to the right event.
Navigate to the `__init__.py` in `events` and add the event name with the callback to the matcher_map:

```python
matcher_map = {
  "app_mention": app_mention_callback,
  # Add more events and callbacks here
}
```

### Messages

Messages are registered almost the same way as Events. Navigate to `src/listeners/messages` and create a new file that
contains the function you would like to run as callback. Here is another sample callback as example:

```python
def goodbye_message_callback(context: BoltContext, say: Say, logger: Logger):
  try:
    farewell = context["matches"][0]
    say(f"{farewell}, see you next time!")
  except Exception as e:
    logger.error(e)
```

Once you have defined a callback function, it needs to be registered to the right text matcher.
Navigate to the `__init__.py` in `messages` and add the string that should trigger the callback to the matcher_map:

```python
matcher_map = {
  r'(hi|hey|hello)': welcome_message_callback,
  r'(goodbye|bye|farewell)': goodbye_message_callback,
}
```

Be aware that unrelated conversations could trigger the bot if the matching phrase is too common! As a default this
bot template will ignore upper and lower case to avoid issues between `Hi` and `hi`. If you need the matcher to react
differently between upper and lower case, edit the `register` function by removing `re.IGNORECASE` from
`app.message(re.compile(pattern, re.IGNORECASE))(callback)`


