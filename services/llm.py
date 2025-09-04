import os
from typing import List, Dict
from openai import OpenAI
from config import OPENAI_API_KEY, OPENAI_MODEL

_client = OpenAI(api_key=OPENAI_API_KEY)

SYSTEM_PROMPT = (
    "You are TaskPilot, an AI task assistant. "
    "Given the user's tasks, extract structured tasks as JSON with fields: "
    "title, due_date (YYYY-MM-DD or null), importance (low|medium|high), "
    "estimated_minutes (int or null). Then return a short prioritized plan."
)

def chat_reply(user_text: str) -> str:
    resp = _client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_text},
        ],
        temperature=0.3,
    )
    return resp.choices[0].message.content
