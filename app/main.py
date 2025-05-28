# app/main.py

from fastapi import FastAPI, Request
from app.parser import process_discharge_summary

app = FastAPI()

@app.get("/ping")
async def ping():
    return {"message": "pong"}

@app.post("/parse")
async def parse_summary(request: Request):
    data = await request.json()
    text = data.get("summary", "")
    if not text:
        return {"error": "No summary provided."}
    
    result = process_discharge_summary(text)
    return result