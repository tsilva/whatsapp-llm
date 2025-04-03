# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv(override=True)

import os
import time
import logging
import uvicorn
import asyncio
from openai import OpenAI
from pyngrok import ngrok
from fastapi import Response
from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse
from twilio.twiml.messaging_response import MessagingResponse

# Load environment variables
WEBHOOK_PORT = int(os.getenv("WEBHOOK_PORT", 8000))
NGROK_AUTH_TOKEN = os.getenv("NGROK_AUTH_TOKEN")
NGROK_DOMAIN = os.getenv("NGROK_DOMAIN")
OPENROUTER_BASE_URL = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
WHITELISTED_NUMBERS = os.getenv("WHITELISTED_NUMBERS", "").split(",")

# Setup basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI()

# Create OpenAI client
client = OpenAI(
    base_url=OPENROUTER_BASE_URL,
    api_key=OPENROUTER_API_KEY
)

async def async_prompt_llm(model_id, messages, temperature=0.0):
    """Async version of prompt_llm to avoid blocking the main thread"""
    try:
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            None, 
            lambda: client.chat.completions.create(
                model=model_id,
                messages=messages,
                temperature=temperature
            )
        )
        return response.choices[0].message.content
    except Exception as e:
        logger.error(f"LLM API error: {str(e)}")
        return "Sorry, I'm having trouble connecting to my brain right now. Please try again in a moment."

@app.post("/whatsapp", response_class=PlainTextResponse)
async def whatsapp_bot(request: Request):
    start_time = time.time()
    
    # Parse form data from the request
    form_data = await request.form()
    incoming_msg = form_data.get("Body", "").strip()
    from_number = form_data.get("From", "")

    # Log incoming message
    logger.info(f"From: {from_number}, Message: {incoming_msg[:30]}...")

    # In case of message not coming from 
    # whitelisted number then return unauthorized
    if not from_number in WHITELISTED_NUMBERS:
        return PlainTextResponse("Unauthorized", status_code=403)
    
    # In case of empty message return bad request
    if not incoming_msg:
        return PlainTextResponse("No message received", status_code=400)
    
    # Prepare response
    resp = MessagingResponse()
    
    # Get LLM response
    try:
        reply = await async_prompt_llm("google/gemini-2.0-flash-001", [
            {"role": "user", "content": incoming_msg}
        ])
        
        # Send reply back to WhatsApp
        resp.message(reply)
        logger.info(f"Response time: {time.time() - start_time:.3f}s")
    except Exception as e:
        logger.error(f"Error processing message: {str(e)}")
        resp.message("Sorry, something went wrong. Please try again later.")

    # Return the Twilio response
    return Response(content=str(resp), media_type="application/xml")

if __name__ == "__main__":
    # Check if in development mode (using debug parameter when running)
    debug_mode = True  # Set this to False in production
    
    if debug_mode:
        # Set ngrok authentication token
        ngrok.set_auth_token(NGROK_AUTH_TOKEN)

        # Start ngrok tunnel
        public_url = ngrok.connect(WEBHOOK_PORT, domain=NGROK_DOMAIN).public_url
        print(f" * ngrok tunnel \"{public_url}\" -> \"http://127.0.0.1:{WEBHOOK_PORT}\"")
        
        # Update the URL in your Twilio WhatsApp Sandbox
        print(f" * Configure your Twilio WhatsApp Sandbox webhook URL to: {public_url}/whatsapp")
    
    # Run the FastAPI application with Uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=WEBHOOK_PORT, reload=debug_mode)