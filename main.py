import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from supabase import create_client, Client
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

app = FastAPI()

# Enable CORS for frontend interaction
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_KEY")
supabase: Client = None

if url and key and url != "your_supabase_url":
    supabase = create_client(url, key)

class ChatMessage(BaseModel):
    content: str

@app.get("/")
async def root():
    return {"message": "AI Chatbot API is running"}

@app.post("/chat")
async def chat(message: ChatMessage):
    # 1. Save user message to Supabase (Optional, don't crash if fails)
    user_msg = {"role": "user", "content": message.content}
    try:
        if supabase:
            supabase.table("messages").insert(user_msg).execute()
    except Exception as e:
        print(f"Supabase Error (User Msg): {e}")
    
    # 2. Generate AI response
    ai_content = f"تم استلام رسالتك: {message.content}. أنا ذكاء اصطناعي بسيط حالياً."
    ai_msg = {"role": "ai", "content": ai_content}
    
    # 3. Save AI message to Supabase (Optional)
    try:
        if supabase:
            supabase.table("messages").insert(ai_msg).execute()
    except Exception as e:
        print(f"Supabase Error (AI Msg): {e}")
    
    return ai_msg

@app.get("/history")
async def get_history():
    if not supabase:
        return []
    
    try:
        response = supabase.table("messages").select("*").order("created_at").execute()
        return response.data
    except Exception as e:
        print(f"Supabase History Error: {e}")
        return []

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
