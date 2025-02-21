from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
# from backend.utils import Chatbot
from backend.utils import AIChatbot
from backend.config import MODEL_NAME, hf_model_name
from concurrent.futures import ThreadPoolExecutor
import uvicorn
import logging
import asyncio

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Pydantic model for input query
class QueryRequest(BaseModel):
    query: str

app = FastAPI()
global chat_bot
executor = ThreadPoolExecutor(max_workers=1)

@app.on_event("startup")
def load_model():
    global chat_bot
    try:
        logger.info("Loading AIChatbot model...")
        chat_bot = AIChatbot(hf_model_name)
        # chat_bot = Chatbot(MODEL_NAME)
        logger.info("Model loaded successfully.")
    except Exception as e:
        logger.error(f"Error loading model: {e}")

@app.get("/")
def health_check():
    logger.info("Health check endpoint hit.")
    return {"Status": "Your API is Successfully Running"}

@app.post("/chats")
async def chat(request: QueryRequest):  # Accepting QueryRequest model
    if chat_bot is None:
        logger.error("Model not loaded.")
        raise HTTPException(status_code=500, detail="Model Not Loaded.")

    logger.info(f"Received query: {request.query}")
    response = await asyncio.get_event_loop().run_in_executor(executor, chat_bot.get_response, request.query)

    last_response = response.split("Human:")[-1].strip()
    logger.info(f"Response generated: {last_response}")
    return {"response": last_response}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8080)
