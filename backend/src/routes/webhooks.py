# Endpoint that would be what Clerk can send a request to and tell us that a new user is created
from fastapi import APIRouter, Request, HTTPException, Depends
from ..database.db import create_challenge_quota
from ..database.models import get_db
from svix.webhooks import Webhook
import os
import json
from sqlalchemy.orm import Session


router = APIRouter()

@router.post("/clerk")
async def handle_user_created(request: Request, db: Session = Depends(get_db)):
    webhook_secret = os.getenv("CLERK_WEBHOOK_SECRET")

    if not webhook_secret:
        raise HTTPException(status_code=500, detail="CLERK_WEBHOOK_SECRET not set")
    
    # This code came from the Clerk documentation that shows us how to validate that the request being sent to webhook is from Clerk
    body = await request.body()
    payload = body.decode("utf-8")
    headers = dict(request.headers)

    # So the using the secret that we included, we're going to be able to determine whether or not the request was indeed from Clerk
    try:
        wh = Webhook(webhook_secret)
        wh.verify(payload, headers)

        # if the lines above raised an error it would not continue to this parts of the code
        data = json.loads(payload) 

        # If clerk sends us any other other event that is not user created, we ignore
        if data.get("type") != "user.created":
            return {"status": "ignored"}
        
        user_data = data.get("data", {})
        user_id = user_data.get("id")

        create_challenge_quota(db, user_id)

        return {"status": "success"}
    
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))