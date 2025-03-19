# api.py
from fastapi import FastAPI
from utils import process_articles, generate_tts

app = FastAPI()

@app.get("/process/{company_name}")
def process_company(company_name: str):
    """API endpoint to process news for a company."""
    data = process_articles(company_name)
    return data

@app.get("/tts/{company_name}")
def get_tts(company_name: str):
    """API endpoint to generate TTS."""
    data = process_articles(company_name)
    summary = " ".join([article["Summary"] for article in data["Articles"]])
    filename = generate_tts(summary)
    return {"audio_file": filename}