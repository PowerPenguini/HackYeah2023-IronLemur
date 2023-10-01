import os
from fastapi import FastAPI
from setup_ai import Ai
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
ai = Ai()
os.environ["OPENAI_API_KEY"] = "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"
origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AiMessage(BaseModel):
    message: str


@app.post("/ai-msg")
async def aimsg(aiMessage: AiMessage):
    return ai.ask(aiMessage.message)