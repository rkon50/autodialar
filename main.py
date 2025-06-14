from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from twilio.rest import Client
import os

app = FastAPI()

account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
twilio_number = os.getenv("TWILIO_PHONE_NUMBER")

if not all([account_sid, auth_token, twilio_number]):
    raise Exception("Twilio credentials are not set in environment variables.")

client = Client(account_sid, auth_token)

class CallRequest(BaseModel):
    to_number: str
    message: str

@app.post("/start_call")
async def start_call(request: CallRequest):
    try:
        call = client.calls.create(
            to=request.to_number,
            from_=twilio_number,
            twiml=f'<Response><Say>{request.message}</Say></Response>'
        )
        return {"message": "Call initiated", "sid": call.sid}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
