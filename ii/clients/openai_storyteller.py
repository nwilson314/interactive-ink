from typing import Generator
from llama_index.core.llms import ChatMessage, MessageRole, ChatResponse

from llama_index.core import Settings
from llama_index.llms.openai import OpenAI

from ii.schema.story_initiation import StoryInitiationRequest


class OpenAIStoryteller:
    def __init__(self):
        self.llm = OpenAI(model="gpt-4o")
        Settings.llm = self.llm

        
    def initiate_story(self, request: StoryInitiationRequest):
        response = self.llm.chat(
            [
                ChatMessage(
                    role=MessageRole.SYSTEM,
                    content=f"You are a story telling AI. You generate stories for the user. Always try to make the story interesting for the user.",
                ),
                ChatMessage(
                    role=MessageRole.USER,
                    content=f"Generate a {request.length} {request.genre} story.",
                )
            ]
        )
        return response.message.content

storyteller = OpenAIStoryteller()

def yield_storyteller() -> Generator[OpenAIStoryteller, None, None]:
    yield storyteller
