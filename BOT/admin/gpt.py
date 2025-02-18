import httpx
import asyncio
from pyrogram import Client, filters
from FUNC.usersdb_func import *
from TOOLS.check_all_func import *

# DeepSeek/OpenRouter Configuration
DEEPSEEK_API_KEY = "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"
API_URL = "https://openrouter.ai/api/v1/chat/completions"

async def fetch_deepseek_response(prompt):
    data = {
        "model": "deepseek/deepseek-r1:free",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.9,
        "top_p": 1,
        "frequency_penalty": 0,
        "presence_penalty": 0,
        "repetition_penalty": 1,
        "top_k": 0,
    }

    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "HTTP-Referer": "https://anujx.cc",  # Replace with your actual domain
        "X-Title": "Your Chat Service",  # Replace with your service name
        "Content-Type": "application/json"
    }

    async with httpx.AsyncClient(timeout=30) as client:
        try:
            response = await client.post(
                API_URL,
                json=data,
                headers=headers
            )
            response.raise_for_status()
            
            completion = response.json()
            if not completion.get('choices'):
                raise ValueError("No choices in response")
            
            return completion['choices'][0]['message']['content']
            
        except httpx.HTTPStatusError as e:
            error_msg = f"HTTP error {e.response.status_code}: {e.response.text}"
            raise Exception(error_msg)
        except json.JSONDecodeError:
            raise Exception("Invalid JSON response from API")

@Client.on_message(filters.command("deepseek", [".", "/"]))
async def cmd_deepseek(Client, message):
    try:
        # Check user permissions
        checkall = await check_all_thing(Client, message)
        if not checkall[0]:
            return
        
        # Get prompt from message
        if message.reply_to_message:
            prompt = message.reply_to_message.text
        else:
            try:
                prompt = message.text.split(" ", 1)[1]
            except IndexError:
                await message.reply_text("<b>⚠️ Invalid Request</b>\nPlease provide a question or message.")
                return

        processing = await message.reply_text("🧠 Processing...")
        
        # Try up to 3 times with exponential backoff
        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = await fetch_deepseek_response(prompt)
                await processing.edit_text(f"<b>{response}</b>")
                return
            except Exception as e:
                if attempt < max_retries - 1:
                    wait_time = 2 ** attempt
                    await asyncio.sleep(wait_time)
                else:
                    await processing.edit_text(f"⚠️ Failed to generate response: {str(e)}")
                    return
                    
    except Exception as e:
        error_msg = f"🚨 Error: {str(e)}"
        await message.reply_text(error_msg)
        import traceback
        await error_log(traceback.format_exc())