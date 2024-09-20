from dotenv import load_dotenv

load_dotenv(override=True)

import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from ii.router import (
    story
)

environment = os.getenv("ENVIRONMENT", "dev")  # Default to 'development' if not set

app = FastAPI()

app.include_router(story.router)

if environment == "dev":
    logger.warning("Running in development mode - allowing CORS for all origins")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
else:
    logger.warning("Running in production mode - disabling CORS")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[""],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


@app.get("/")
async def root():
    return {
        "message": "Hello, World!",
    }
