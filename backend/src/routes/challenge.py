# API endpoints
from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel
from sqlalchemy.orm import Session
from ..database.db import (
    get_challenge_quota,
    create_challenge,
    create_challenge_quota,
    reset_quota_if_needed,
    get_user_challenge
)
from ..utils import authenticate_and_get_user_details
from ..database.models import get_db
import json
from datetime import datetime

router = APIRouter()

# The post endpoint that the user can call to generate a challenge
# We first define a schema - something that FastAPI can ue to validate that the data being sent to the endpoint is correct
# This ensures that the user will send the correct type of data
class ChallengeRequest(BaseModel):
    difficulty: str

    class Config:
        json_schema_extra = {"example": {"difficulty": "easy"}}

@router.post("/generate-challenge")
async def generate_challenge(request: ChallengeRequest, db: Session = Depends(get_db)):
    try:
        # This will authenticate the user and get their details
        user_details = authenticate_and_get_user_details(request)
        user_id = user_details.get("user_id")
        quota = get_challenge_quota(db, user_id)

        # if they don't have a quota yet we make one
        if not quota:
            create_challenge_quota(db, user_id)

        # We reset their quota so that if it is 0 but its been more than 24 hours
        quota = reset_quota_if_needed(db, quota)

        # We check their quota
        if quota.quota_remaining <= 0:
            raise HTTPException(status_code=429, details="Quota exhausted")

        challenge_data = None

        # TODO: Generate Challenge

        quota.remaining_quota -= 1
        db.commit()

        return challenge_data

    except Exception as e:
        raise HTTPException(status_code=400, detail="Bad Request")


@router.get("/my-history")
# This automatically gets the db session for us
async def my_history(request: Request, db: Session = Depends(get_db)):
    # This will authenticate the user and get their details
    user_details = authenticate_and_get_user_details(request)
    user_id = user_details.get("user_id")

    challenges = get_user_challenge(db, user_id)
    return {"challenges": challenges}


@router.get("/quota")
async def get_quota(request: Request, db: Session = Depends(get_db)):
    user_details = authenticate_and_get_user_details(request)
    user_id = user_details.get("user_id")

    quota = get_challenge_quota(db, user_id)

    if not quota:
        return {
            "user_id": user_id,
            "quota_remaining": 0,
            "last_reset_date": datetime.now()
        }
    
    quota = reset_quota_if_needed(db, quota)
    return quota