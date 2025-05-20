# app/main.py

from fastapi import FastAPI

# Create the FastAPI app instance
app = FastAPI()

# Define a simple test endpoint
@app.get("/ping")
async def ping():
    return {"message": "pong"}