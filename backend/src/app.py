# Here we setup the fast API - framework that allows us to create API in python
from fastapi import FastAPI, Request, Response

# This makes sure that our frontend can send requests to our backend
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# The * tells that we allow anybody to send requests to our backend
app.add_middleware(CORSMiddleware, 
                    allow_origins=["*"], 
                    allow_credentials=True, 
                    allow_methods=["*"], 
                    allow_headers=["*"])

