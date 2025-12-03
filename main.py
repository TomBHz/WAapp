from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import httpx
from dotenv import load_dotenv

load_dotenv()

WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN")
PHONE_NUMBER_ID = os.getenv("WHATSAPP_PHONE_NUMBER_ID")

if not WHATSAPP_TOKEN:
    raise RuntimeError("WHATSAPP_TOKEN não configurado no .env")
if not PHONE_NUMBER_ID:
    raise RuntimeError("WHATSAPP_PHONE_NUMBER_ID não configurado no .env")

WHATSAPP_URL = f"https://graph.facebook.com/v22.0/{PHONE_NUMBER_ID}/messages"

app = FastAPI(title="WhatsTime Backend")

class SendRequest(BaseModel):
    to: str
    message: str

@app.get("/")
def root():
    return {"status": "ok", "app": "WhatsTime backend"}

@app.post("/api/send")
async def send_message(req: SendRequest):
    payload = {
        "messaging_product": "whatsapp",
        "to": req.to,
        "type": "text",
        "text": {"body": req.message}
    }

    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }

    async with httpx.AsyncClient() as client:
        r = await client.post(WHATSAPP_URL, json=payload, headers=headers)

        if 200 <= r.status_code < 300:
            return {"success": True, "response": r.json()}

        return {"success": False, "status": r.status_code, "detail": r.json()}
