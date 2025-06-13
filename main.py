from fastapi import FastAPI
from pydantic import BaseModel
from twilio.rest import Client
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

app = FastAPI()

# Twilio credentials
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

class CallRequest(BaseModel):
    phone_number: str

@app.post("/start_call")
def start_call(req: CallRequest):
    call = client.calls.create(
        url="http://demo.twilio.com/docs/voice.xml",
        to=req.phone_number,
        from_=TWILIO_PHONE_NUMBER
    )
    return {"message": f"Call initiated to {req.phone_number}", "call_sid": call.sid}
