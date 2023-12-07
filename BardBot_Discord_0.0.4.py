import discord
import requests
import json
from discord.ext import commands
from google.cloud import language_v1
from google.oauth2 import service_account

# Set your API keys
google_cloud_api_key_path = "bardbot.json"
bot_token = "MTE4MjAwMjc5Njc3NDU2MzkyMg.GgB6Y8.dnLt_mV31xiNadp7qHHzeGWhb9QTuZ8LCOv_A0"
target_project_id = "bardbot-407318"
google_bard_api_key = "AIzaSyA0-MwEO8HxXoxxWyl8GdEDGGE-zPJ4-SU"

# Initialize the Google Cloud Natural Language API client
credentials = service_account.Credentials.from_service_account_file(google_cloud_api_key_path)
language_client = language_v1.LanguageServiceClient(credentials=credentials)

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
    # Call the Google Bard API with the provided question
    response = get_bard_response(question)

    # Send the response back to the Discord channel
    await ctx.send(response)

def get_bard_response(question):
    # Google Bard API endpoint
    bard_api_url = "https://language.googleapis.com/v1/documents:analyzeSentiment"

    # Prepare the request payload
    payload = {
        "question": {
            "text": question
        }
    }

    # Include your Google Bard API key in the request headers
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {google_bard_api_key}"
    }

    # Make the API request
    response = requests.post(bard_api_url, json=payload, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response and extract the answer
        answer = response.json().get("answer", "No answer found.")
        return answer
    else:
        # Handle errors
        return f"Error: Unable to get answer. Status code: {response.status_code}"

# Run the bot
bot.run(bot_token)
