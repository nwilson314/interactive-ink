from typing import Generator
from llama_index.core.llms import ChatMessage, MessageRole, ChatResponse

from llama_index.core import Settings
from llama_index.llms.openai import OpenAI

from ii.schema.enums import StoryLength
from ii.schema.story_initiation import StoryInitiationRequest


class OpenAIStoryteller:
    def __init__(self):
        self.llm = OpenAI(model="gpt-4o", temperature=0.9)
        Settings.llm = self.llm

    def initiate_story(self, request: StoryInitiationRequest):
        messages = [
            ChatMessage(
                role=MessageRole.SYSTEM,
                content=f"You are a story telling AI. You generate stories for the user. Always try to make the story both unique and interesting for the user. \
                        The story will be of the choose your own adventure variety. The story will be {request.length.value} {request.genre.value}. \
                        There will be {StoryLength.num_exchanges(request.length)} action events for the user to choose from over the course of the story. \
                        Generate an initial response and then remake it with completely new characters and settings. Only include the second response.",
            ),
            ChatMessage(
                role=MessageRole.USER,
                content=f"To start, generate the first piece of plot. Do not yet generate the list of available actions. That will come next. Provide only the story content.",
            ),
        ]
        response = self.llm.chat(messages)

        return response.message.content


storyteller = OpenAIStoryteller()


def yield_storyteller() -> Generator[OpenAIStoryteller, None, None]:
    yield storyteller
