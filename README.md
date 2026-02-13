<div align="center">
  <img src="logo.jpg" alt="whatsapp-llm" width="256"/>

  # whatsapp-llm

  [![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
  [![Python](https://img.shields.io/badge/Python-3.8+-3776ab.svg)](https://python.org)
  [![FastAPI](https://img.shields.io/badge/FastAPI-009688.svg)](https://fastapi.tiangolo.com)

  **🤖💬 Bridge WhatsApp to AI — send a message, get an intelligent response instantly 🚀**

  [Getting Started](#-quick-start) · [Configuration](#%EF%B8%8F-configuration) · [How It Works](#-how-it-works)
</div>

---

## Overview

whatsapp-llm connects WhatsApp to AI language models through Twilio webhooks. Send a message on WhatsApp, get an AI response back instantly. Uses OpenRouter to access models like Gemini, Claude, GPT, and more.

## Features

- **Instant AI responses** - Messages processed through OpenRouter's API with support for 100+ models
- **Secure access** - Whitelist-based number filtering ensures only authorized users can interact
- **Zero-config tunneling** - Built-in ngrok integration exposes your local server for Twilio callbacks
- **Async processing** - Non-blocking LLM calls keep the webhook responsive

## Quick Start

```bash
# Clone and install
git clone https://github.com/tsilva/whatsapp-llm.git
cd whatsapp-llm
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your API keys

# Run
python main.py
```

The server starts and displays an ngrok URL. Add `{ngrok-url}/whatsapp` as your Twilio WhatsApp Sandbox webhook.

## Configuration

Create a `.env` file with the following variables:

| Variable | Required | Description |
|----------|----------|-------------|
| `OPENROUTER_API_KEY` | Yes | Your [OpenRouter](https://openrouter.ai) API key |
| `NGROK_AUTH_TOKEN` | Yes | Your [ngrok](https://ngrok.com) authentication token |
| `WHITELISTED_NUMBERS` | Yes | Comma-separated WhatsApp numbers (format: `whatsapp:+12345678900`) |
| `NGROK_DOMAIN` | No | Custom ngrok domain if you have one |
| `WEBHOOK_PORT` | No | Server port (default: 8000) |
| `OPENROUTER_BASE_URL` | No | OpenRouter API base URL (default: `https://openrouter.ai/api/v1`) |

## How It Works

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  WhatsApp   │────▶│   Twilio    │────▶│   FastAPI   │────▶│ OpenRouter  │
│   Message   │     │   Webhook   │     │   Server    │     │     LLM     │
└─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘
                                               │                    │
                                               │◀───────────────────┘
                                               │         AI Response
┌─────────────┐     ┌─────────────┐            │
│  WhatsApp   │◀────│   Twilio    │◀───────────┘
│   Reply     │     │   TwiML     │
└─────────────┘     └─────────────┘
```

1. User sends a WhatsApp message to your Twilio number
2. Twilio forwards the message to your webhook endpoint
3. Server validates the sender against the whitelist
4. Message is sent to the LLM via OpenRouter
5. AI response is wrapped in TwiML and returned to Twilio
6. User receives the reply on WhatsApp

## Twilio Setup

1. Create a [Twilio account](https://www.twilio.com) and activate the WhatsApp Sandbox
2. Run `python main.py` to get your ngrok URL
3. In Twilio Console → Messaging → WhatsApp Sandbox, set the webhook URL to `{ngrok-url}/whatsapp`
4. Send the join code to the Sandbox number from your WhatsApp
5. Start chatting with your AI assistant

## Requirements

- Python 3.8+
- Twilio account with WhatsApp Sandbox access
- OpenRouter API key
- ngrok account (free tier works)

## License

[MIT](LICENSE) © Tiago Silva
