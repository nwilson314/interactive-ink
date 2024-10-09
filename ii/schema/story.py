import uuid
from typing import Optional

from pydantic import BaseModel, Field

from ii.schema.enums import StoryGenre, StoryLength


class StoryInitiationRequest(BaseModel):
    genre: StoryGenre
    length: StoryLength


class Story(BaseModel):
    id_: str = Field(default_factory=lambda: str(uuid.uuid4())) 
    blocks: list["StoryBlock"]
    genre: StoryGenre
    length: StoryLength


BLOCK_TEMPLATE = """
BLOCK
===
CONTENT: {content}
CHOICES: {choices}
CHOSEN: {chosen}
"""


class StorySegment(BaseModel):
    content: str = Field(
        description="The plot of the story for the current segment. The plot should be no longer than 5 sentences."
    )
    choices: list[str] = Field(
        default=[],
        description="The list of actions the protaganist can take that will shape the plot and actions of the next segment.",
    )


class StoryBlock(BaseModel):
    id_: str = Field(default_factory=lambda: str(uuid.uuid4()))
    segment: StorySegment
    chosen: Optional[str] = None
    block_template: str = BLOCK_TEMPLATE

    def __str__(self):
        return self.block_template.format(
            plot=self.segment.content,
            actions=", ".join(self.segment.choices),
            choice=self.chosen or "",
        )