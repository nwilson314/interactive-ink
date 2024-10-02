from uuid import UUID

from pydantic import BaseModel

from ii.schema.chat_message import ChatMessage
from ii.schema.enums import StoryGenre, StoryLength


class StoryInitiationRequest(BaseModel):
    genre: StoryGenre
    length: StoryLength


class StoryInitiationResponse(BaseModel):
    story_id: UUID
    initiation_request: StoryInitiationRequest
    messages: list[ChatMessage]


class ContinueStoryRequest(BaseModel):
    story_id: UUID
    messages: list[ChatMessage]


class ContinueStoryResponse(BaseModel):
    story_id: UUID
    messages: list[ChatMessage]