from discord.ext import commands
from discord_slash import SlashCommand
from google.cloud import language_v1

# Set your API keys
google_cloud_api_key = ""
bot_token = ""

# Initialize the Discord bot with intents and commands extension
intents = commands.Bot(command_prefix='$', intents=commands.Intents.all())
slash = SlashCommand(intents, sync_commands=True)

# Initialize the Google Cloud Natural Language API client
client = language_v1.LanguageServiceClient.from_service_account_info(google_cloud_api_key, target_project_id="your_project_id")

@intents.event
async def on_ready():
    print(f'We have logged in as {intents.user.name}')

@intents.command(name='analyze_sentiment')
async def analyze_sentiment(ctx, *, text: str):
    document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)
    sentiment = client.analyze_sentiment(document=document).document_sentiment

    await ctx.send(f'Sentiment score: {sentiment.score}, Magnitude: {sentiment.magnitude}')

# Run the bot
intents.run(bot_token)
