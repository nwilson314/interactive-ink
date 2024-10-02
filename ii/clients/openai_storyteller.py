from typing import Generator
from uuid import uuid4

from llama_index.core.llms import ChatMessage as ChatGPTMessage, MessageRole
from llama_index.core import Settings
from llama_index.llms.openai import OpenAI

from ii.schema.chat_message import ChatMessage
from ii.schema.enums import StoryLength
from ii.schema.story import StoryInitiationRequest, StoryInitiationResponse, ContinueStoryRequest, ContinueStoryResponse


class OpenAIStoryteller:
    def __init__(self):
        self.llm = OpenAI(model="gpt-4o", temperature=0.9)
        Settings.llm = self.llm

    def initiate_story(self, request: StoryInitiationRequest) -> StoryInitiationResponse:
        messages = [
            ChatGPTMessage(
                role=MessageRole.SYSTEM,
                content=f"You are a story telling AI. You generate stories for the user. Always try to make the story both unique and interesting for the user. \
                        The story will be of the choose your own adventure variety. The story will be of {request.length.value} length and in the genre {request.genre.value}. \
                        There will be {StoryLength.num_exchanges(request.length)} action events for the user to choose from over the course of the story. \
                        Generate an initial response and then remake it with completely new characters and settings. Only include the second response.",
            ),
            ChatGPTMessage(
                role=MessageRole.USER,
                content=f"To start, generate the first piece of plot. Do not yet generate the list of available actions. That will come next. Provide only the story content.",
            ),
        ]
        response = self.llm.chat(messages)
        messages.append(response.message)

        return StoryInitiationResponse(
            story_id=uuid4(),
            initiation_request=request,
            messages=[
                ChatMessage(
                    role=message.role,
                    content=message.content,
                )
                for message in messages
            ]
        )


storyteller = OpenAIStoryteller()


def yield_storyteller() -> Generator[OpenAIStoryteller, None, None]:
    yield storyteller
