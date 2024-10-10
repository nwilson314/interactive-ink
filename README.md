# Interactive Ink
The backend for Interactive Ink. Written in Python making use of FastAPI, Llama Index and OpenAI. Interactive Ink is a platform that generates unique, AI-driven choose-your-own-adventure stories.

Frontend code [here](https://github.com/nwilson314/interactive-ink-frontend).

A running demo can be found here: https://interactive-ink.fly.dev/ (startup times may be slow initially).

## Running
```bash
poetry run uvicorn ii:app --reload
```