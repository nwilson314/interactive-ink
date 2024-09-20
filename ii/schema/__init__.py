from pydantic import BaseModel

from ii.schema.enums import StoryGenre, StoryLength


class StoryInitiationRequest(BaseModel):
    genre: StoryGenre
    length: StoryLength
