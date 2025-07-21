


# Sentiment Chatbot with Azure AI Integration

## Overview

This project integrates a chatbot with Azure’s AI-as-a-Service platform, specifically utilizing the **Azure AI Language Service** for **sentiment analysis**. The chatbot interacts with users by analyzing the sentiment of their inputs (positive, neutral, or negative) and returns a tailored response based on the analysis. The bot utilizes Azure's Text Analytics API for the sentiment analysis functionality, providing a more intelligent and engaging interaction for users.

## Requirements

Before you begin, make sure you have the following:

- **Python 3.x** installed on your system.
- **Azure account** with access to Azure Cognitive Services (you can sign up for a free Azure account).
- **Bot Framework SDK** and **Azure SDK** for Python installed.

### Install the dependencies:

```bash
pip install azure-ai-textanalytics
pip install botbuilder-core
```

## Setup

### Step 1: Set up your Azure Cognitive Services

1. Sign up for a **free Azure account** (if you haven’t already) at [Azure Free Account](https://azure.microsoft.com/en-us/free).
2. Create a **Text Analytics** resource under Azure Cognitive Services in your Azure portal.
3. Copy your **API Key** and **Endpoint** from the resource's "Keys and Endpoints" section.

### Step 2: Set up environment variables

Set up the environment variables to securely store the API key and endpoint:

```bash
SET MicrosoftAPIKey=YOUR_API_KEY
SET MicrosoftAIServiceEndpoint=YOUR_ENDPOINT
```

Replace `YOUR_API_KEY` and `YOUR_ENDPOINT` with the values you obtained from Azure.

### Step 3: Run the chatbot

1. Clone this repository or download the provided Python script.
2. Run the chatbot using the command:

```bash
python chatbot.py
```

3. Test the bot using the **Bot Framework Emulator** or deploy it to a web server to interact with real users.

## Features

- **Sentiment Analysis**: The bot analyzes user input and classifies it as positive, neutral, or negative.
- **Custom Responses**: Based on the sentiment score, the bot returns personalized responses.
- **Bot Framework Integration**: Built using the Microsoft Bot Framework, allowing for easy extension and integration with other services.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
