import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
# from sb_client import create_client, Client
import supabase as sb
from datetime import datetime
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    supabase_url: str
    supabase_key: str

    # This tells Pydantic to look for a .env file
    model_config = SettingsConfigDict(env_file="/Users/Senne/Documents/VSCode/wordable_new/backend/.env")


# Create a singleton instance
settings = Settings()




app = FastAPI(title="Vocabulary Practice API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173/"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# sb_client configuration
sb_client_URL = settings.supabase_url
sb_client_KEY = settings.supabase_key

if not sb_client_URL or not sb_client_KEY:
    raise ValueError("sb_client_URL and sb_client_KEY must be set in environment variables")

sb_client: sb.Client = sb.Client(sb_client_URL, sb_client_KEY)

# Pydantic models
class VocabularyCreate(BaseModel):
    word: str
    translation: str
    language: str

class VocabularyCreateList(BaseModel):
    words: list[VocabularyCreate]

class PracticeRecord(BaseModel):
    vocabulary_id: int
    is_correct: int

# Routes
@app.get("/api/health")
async def health():
    return {"status": "ok"}

# get wordlist
@app.get("/api/vocabulary/wordlists")
async def get_vocabulary():
    try:
        response = sb_client.table("vocabulary").select("*").execute()
        return response.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/vocabulary/wordlists")
async def add_vocabulary(vocab: VocabularyCreateList):
    try:
        response = sb_client.table("vocabulary").insert({
            "word": vocab.word,
            "translation": vocab.translation,
            "language": vocab.language,
            "created_at": datetime.utcnow().isoformat()
        }).execute()
        return {"message": "Vocabulary added successfully", "data": response.data}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/api/vocabulary/{vocab_id}")
async def delete_vocabulary(vocab_id: int):
    try:
        sb_client.table("vocabulary").delete().eq("id", vocab_id).execute()
        return {"message": "Vocabulary deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/practice")
async def record_practice(practice: PracticeRecord):
    try:
        response = sb_client.table("practice_sessions").insert({
            "vocabulary_id": practice.vocabulary_id,
            "is_correct": practice.is_correct,
            "created_at": datetime.utcnow().isoformat()
        }).execute()
        return {"message": "Practice recorded", "data": response.data}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/statistics")
async def get_statistics():
    try:
        # Get total words
        total_words_response = sb_client.table("vocabulary").select("count", count="exact").execute()
        total_words = total_words_response.count or 0
        
        # Get all practice sessions
        practice_response = sb_client.table("practice_sessions").select("*").execute()
        total_attempts = len(practice_response.data) if practice_response.data else 0
        
        # Count correct attempts
        correct_attempts = sum(1 for p in (practice_response.data or []) if p.get("is_correct") == 1)
        
        accuracy = (correct_attempts / total_attempts * 100) if total_attempts > 0 else 0
        
        return {
            "total_words": total_words,
            "total_attempts": total_attempts,
            "correct_attempts": correct_attempts,
            "accuracy": round(accuracy, 2)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
