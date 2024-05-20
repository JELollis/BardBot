import discord
import google.cloud
import requests
import json

from discord.ext import commands
from google.cloud import language_v1

# Set your API keys (still required for Google Cloud Natural Language API)
google_cloud_api_key_path = "bardbot.json"
bot_token = "discord_bardbot.json"
#target_project_id = ""

# Load the service account credentials from the JSON file
with open(google_cloud_api_key_path, 'r') as f:
    credentials = json.load(f)

# Initialize the Google Cloud Natural Language API client
language_client = language_v1.LanguageServiceClient.from_service_account_info(credentials)

# Initialize the Discord bot with intents and commands extension
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='/', intents=intents)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user.name}')

@bot.command(name='analyze_sentiment')
async def analyze_sentiment(ctx, text: str):
    document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)
    sentiment = language_client.analyze_sentiment(document=document).document_sentiment

    await ctx.send(f'Sentiment score: {sentiment.score}, Magnitude: {sentiment.magnitude}')

@bot.command(name='Bard')
async def bard_command(ctx, *, question: str):
    # Inform the user that a public Bard API is not currently available
    await ctx.send("**Currently, there is no public API for Google Bard.**  Would you like to try using the Google Cloud Natural Language API for sentiment analysis instead?")

# Run the bot
bot.run(bot_token)
