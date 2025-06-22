# app/main.py

from fastapi import FastAPI, Request, HTTPException
from app.parser import process_discharge_summary

app = FastAPI()

@app.get("/ping")
async def ping():
    return {"message": "pong"}

@app.post("/parse")
async def parse_summary(request: Request):
    try:
        data = await request.json()
        text = data.get("summary", "")
        if not text.strip():
            raise HTTPException(status_code=400, detail="Summary field is required.")
        return process_discharge_summary(text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))