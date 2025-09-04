# TaskPilot — AI Task Prioritization Assistant

TaskPilot is a ChatGPT‑style web app that parses free‑form to‑dos, extracts structured tasks,
and generates a prioritized schedule using a lightweight scoring model and an LLM.

## Quick start

1. Create a virtualenv and install requirements
   ```bash
   pip install -r requirements.txt
   python -m spacy download en_core_web_sm
   ```
2. Copy `.env.example` to `.env` and set your API key(s)
3. Run
   ```bash
   python app.py
   ```
4. Open http://127.0.0.1:5000

## Environment

- `OPENAI_API_KEY` (required)
- `OPENAI_MODEL` (optional, default: gpt-4o-mini)
- `FLASK_ENV` (optional, default: development)

## Tech

- Backend: Flask, Python
- LLM: OpenAI Chat Completions
- NLP: spaCy (optional)
- Frontend: HTML + JS fetch
- Scheduling: simple heuristic (due date, importance, effort)

## Notes

- spaCy is optional. If the model is not downloaded, the app falls back to a regex/keyword parser.
- All code is contained in this repo and can be deployed to any Python host.
