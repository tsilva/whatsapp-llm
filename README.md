# 🤖 whatsapp-llm

<p align="center">
  <img src="logo.jpg" alt="Logo" width="400"/>
</p>


🔹 Connect your WhatsApp to powerful AI language models through a simple webhook service

## 📖 Overview

WhatsApp-LLM creates a bridge between WhatsApp and AI language models like Google's Gemini. It uses FastAPI to create a webhook that receives messages from WhatsApp via Twilio, processes them through AI models via OpenRouter, and returns the responses back to the user. Perfect for creating your own AI assistant accessible through WhatsApp messaging.

## 🚀 Installation

```bash
# Clone the repository
git clone https://github.com/tsilva/whatsapp-llm.git
cd whatsapp-llm

# Install dependencies
pip install -r requirementex.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your API keys and configuration
```

## 🛠️ Usage

1. Configure your environment variables in the `.env` file:
   - `OPENROUTER_API_KEY`: Your OpenRouter API key
   - `NGROK_AUTH_TOKEN`: Your ngrok authentication token
   - `WHITELISTED_NUMBERS`: Comma-separated list of WhatsApp numbers allowed to use the service
   - `NGROK_DOMAIN`: Your custom ngrok domain (if available)

2. Run the application:
   ```bash
   python main.py
   ```

3. The application will start and display a ngrok URL. Configure this URL in your Twilio WhatsApp Sandbox settings as the webhook URL with the `/whatsapp` endpoint.

4. Send a message to your WhatsApp Sandbox number, and you'll receive a response from the AI model.

## 📄 License

This project is licensed under the [MIT License](LICENSE).