from typing import Generator
from uuid import uuid4

from llama_index.core import Settings
from llama_index.core.prompts import PromptTemplate
from llama_index.llms.openai import OpenAI

from ii.schema.enums import StoryLength
from ii.schema.story import StorySegment, StoryBlock, StoryInitiationRequest, Story


SEGMENT_GENERATION_TEMPLATE = """
You are working with a human to create a story in the style of choose your own adventure.

The human is playing the role of the protaganist in the story which you are tasked to
help write. To create the story, we do it in steps, where each step produces a STORYBLOCK.
Each STORYBLOCK consists of a CONTENT, a set of CHOICES that the protaganist can take, and the
chosen CHOICE. The story will have a total of {story_length} STORYBLOCKs. There are 
currently NUM_BLOCKS = {num_blocks}. The genre is {genre}.

Below we attach the history of the adventure so far.

PREVIOUS STORYBLOCKs:
---
{story}

If there are no previous STORYBLOCKs (i.e. NUM_BLOCKS == 0), generate an initial plot. Then take 
that initial plot and characters and start over. DO NOT REUSE ANYTHING. Give the 
protaganist a name and an interesting challenge to solve.

Continue the story by generating the next block's CONTENT and set of CHOICES. 


Use the provided data model to structure your output.
"""


class OpenAIStoryteller:
    def __init__(self):
        self.llm = OpenAI(model="gpt-4o", temperature=0.9)
        Settings.llm = self.llm

    def initiate_story(self, request: StoryInitiationRequest) -> None:
        prompt_template = PromptTemplate(SEGMENT_GENERATION_TEMPLATE)
        segment = self.llm.structured_predict(
            StorySegment,
            prompt_template,
            story="",
            story_length=StoryLength.num_exchanges(request.length.value),
            num_blocks=0,
            genre=request.genre.value,
        )

        return Story(
            id_=str(uuid4()),
            blocks=[StoryBlock(segment=segment)],
            genre=request.genre,
            length=request.length,
        )


storyteller = OpenAIStoryteller()


def yield_storyteller() -> Generator[OpenAIStoryteller, None, None]:
    yield storyteller
