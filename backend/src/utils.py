# This will allow us to authenticate using clerk
# How this works:
# Frontend
#   clerk authenticate
#   issue jwt token
#   sent to the backend

# Backend
#   connect to clerk using the key
#   ask clerk if the token is valid

from fastapi import HTTPException
from clerk_backend_api import Clerk, AuthenticateRequestOptions
import os

# This will look for the presence of the environment file to load the key
from dotenv import load_dotenv

load_dotenv()

# Tell clerk that we are the owner of the app and would allow us to do token operations
clerk_sdk = Clerk(bearer_auth=os.getenv("CLERK_SECRET_KEY"))

# We can use this whenever a request is sent to our backend to verify the validity of the request
def authenticate_and_get_user_details(request):
    try:
        request_state = clerk_sdk.authenticate_request(
            request, 
            AuthenticateRequestOptions(
                authorized_parties=["http://localhost:5173"],
                jwt_key=os.getenv("JWT_KEY")
            )
        )
        if not request_state.is_signed_in:
            raise HTTPException(status_code=401, details="Invalid token")

        # the request state will store a token and within that token it will contain the particular user whi it belongs to under the field called sub
        user_id = request_state.payload.get("sub")

        return {"user_id": user_id}

    except Exception as e:
        raise HTTPException(status_code=500, detail="Invalid credentials")
    