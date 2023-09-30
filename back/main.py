import os
from fastapi import FastAPI
from setup_ai import Ai
from pydantic import BaseModel

app = FastAPI()
ai = Ai()
os.environ["OPENAI_API_KEY"] = "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"


class AiMessage(BaseModel):
    message: str


@app.post("/ai-msg")
async def aimsg(aiMessage: AiMessage):
    return ai.ask(aiMessage.message)