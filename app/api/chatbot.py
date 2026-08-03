from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/chatbot", tags=["Chatbot"])

class ChatRequest(BaseModel):
    message: str

@router.post("/query")
async def ask_retail_bot(payload: ChatRequest):
    user_query = payload.message.lower()
    
    try:
        # In production, replace this with your LLM / OpenAI API call
        # e.g., response = await openai.ChatCompletion.acreate(...)
        
        if "revenue" in user_query or "sales" in user_query:
            bot_reply = "📊 Checking the warehouse... Our top category this month is Electronics, contributing 42% of total sales."
        elif "inventory" in user_query or "stock" in user_query:
            bot_reply = "⚠️ Warning: Stock levels for 'Wireless Headphones' have dropped below 15 units in the East Warehouse."
        else:
            bot_reply = f"Hello! I am your Retail Operations Copilot. I can help analyze performance metrics or write query plans. You said: '{payload.message}'"
            
        return {"reply": bot_reply}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chatbot service offline: {str(e)}")
