# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

WhatsApp-LLM is a webhook service that bridges WhatsApp messaging with AI language models. It receives WhatsApp messages via Twilio, processes them through OpenRouter's API (using OpenAI-compatible client), and sends responses back.

## Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application (starts FastAPI server with ngrok tunnel)
python main.py
```

## Architecture

Single-file FastAPI application (`main.py`) with these components:

- **Webhook endpoint** (`POST /whatsapp`): Receives Twilio WhatsApp messages, validates sender against whitelist, calls LLM, returns TwiML response
- **LLM integration**: Uses OpenAI client pointed at OpenRouter API (`async_prompt_llm` function)
- **Tunnel**: ngrok exposes local server for Twilio webhook callbacks

## Key Configuration

Environment variables loaded from `.env` (see `.env.example`):
- `OPENROUTER_API_KEY`: Required for LLM API access
- `NGROK_AUTH_TOKEN`: Required for tunnel in debug mode
- `WHITELISTED_NUMBERS`: Comma-separated WhatsApp numbers (format: `whatsapp:+12345678900`)
- `NGROK_DOMAIN`: Optional custom ngrok domain

## Maintenance Notes

- README.md must be kept up to date with any significant project changes
