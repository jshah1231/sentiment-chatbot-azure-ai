import os
import logging
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
from botbuilder.core import ActivityHandler, TurnContext
from botbuilder.ai.luis import LuisRecognizer, LuisApplication, LuisPredictionOptions

# Fetch API key and endpoint from environment variables
# These are crucial for securely connecting to the Azure Cognitive Service API
api_key = os.environ.get("MicrosoftAPIKey")
endpoint = os.environ.get("MicrosoftAIServiceEndpoint")

# Ensure that both the API key and endpoint are properly set, if not, raise an error
if not api_key or not endpoint:
    raise ValueError("Please set the API key and endpoint as environment variables.")

# Set up the Azure Text Analytics client
def authenticate_client():
    """
    Authenticate the Azure Text Analytics client using the provided API key and endpoint.
    The client is responsible for interacting with Azure's Cognitive Services Text Analytics API.
    """
    # AzureKeyCredential stores the API key for secure access to the service
    credential = AzureKeyCredential(api_key)
    
    # Create and return an authenticated instance of TextAnalyticsClient
    client = TextAnalyticsClient(endpoint=endpoint, credential=credential)
    return client

# Create a function to analyze sentiment
def analyze_sentiment(client, text):
    """
    Analyzes the sentiment of the provided text using Azure's Sentiment Analysis API.
    It returns the sentiment (positive, negative, or neutral) and confidence scores for each sentiment type.

    :param client: Authenticated instance of TextAnalyticsClient
    :param text: Text input to analyze for sentiment
    :return: Sentiment type and confidence scores for positive, negative, and neutral
    """
    try:
        # Call the Azure service to analyze sentiment, passing the text in a list
        response = client.analyze_sentiment(documents=[text])[0]
        
        # Retrieve the sentiment classification and confidence scores
        sentiment = response.sentiment
        positive_score = response.confidence_scores.positive
        negative_score = response.confidence_scores.negative
        neutral_score = response.confidence_scores.neutral

        # Return the sentiment classification and associated confidence scores
        return sentiment, positive_score, negative_score, neutral_score

    except Exception as e:
        # If an error occurs during sentiment analysis, log the error and return None values
        logging.error(f"Error during sentiment analysis: {str(e)}")
        return None, None, None, None

# Define the Chatbot class using Bot Framework's ActivityHandler
class SentimentChatBot(ActivityHandler):
    """
    A chatbot class that extends ActivityHandler and responds to user messages.
    The chatbot integrates Azure's Sentiment Analysis API to analyze user input
    and provide sentiment-based responses.
    """

    def __init__(self):
        """
        Initialize the SentimentChatBot instance. This includes setting up the Azure client for sentiment analysis.
        """
        super().__init__()
        
        # Authenticate and create the TextAnalyticsClient instance
        self.client = authenticate_client()

    async def on_message_activity(self, turn_context: TurnContext):
        """
        Handles incoming messages from users. This method is triggered when the bot receives a message.
        It analyzes the sentiment of the message and sends a corresponding sentiment-based response.

        :param turn_context: The context for the current activity, including the user message
        """
        # Retrieve and clean the user input (removing any leading/trailing whitespace)
        user_input = turn_context.activity.text.strip()
        
        # Perform sentiment analysis on the user input text
        sentiment, pos_score, neg_score, neutral_score = analyze_sentiment(self.client, user_input)

        # Prepare a custom response based on the sentiment result
        if sentiment == "positive":
            # If the sentiment is positive, respond with a cheerful message
            response = f"Your message seems positive! 😊 (Positive score: {pos_score:.2f})"
        elif sentiment == "negative":
            # If the sentiment is negative, respond with a sympathetic message
            response = f"Your message seems negative. 😟 (Negative score: {neg_score:.2f})"
        elif sentiment == "neutral":
            # If the sentiment is neutral, respond with an inquisitive message
            response = f"Your message seems neutral. 🤔 (Neutral score: {neutral_score:.2f})"
        else:
            # If sentiment cannot be classified, return a generic message
            response = "I'm not sure how to analyze that message."

        # Send the crafted response back to the user
        await turn_context.send_activity(response)

# Main method to run the chatbot
if __name__ == "__main__":
    from botbuilder.core import BotFrameworkAdapter, BotFrameworkAdapterSettings

    # Set up the bot adapter with your Microsoft App credentials
    # These credentials are required to connect to the Microsoft Bot Framework
    settings = BotFrameworkAdapterSettings(app_id="YOUR_APP_ID", app_password="YOUR_APP_PASSWORD")
    adapter = BotFrameworkAdapter(settings)

    # Create an instance of the SentimentChatBot
    bot = SentimentChatBot()

    # Define the method that will handle bot turns
    async def on_turn(turn_context: TurnContext):
        """
        Handles each turn (interaction) with the bot. The bot responds based on user input.
        """
        await bot.on_turn(turn_context)

    # Bind the on_turn function to the adapter to process messages
    adapter.on_turn(on_turn)

    # This line is a placeholder for actual web framework integration
    # In a real-world scenario, you'd integrate this bot with a web server (Flask, FastAPI, etc.)
    print("Bot is running...")

