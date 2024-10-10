from typing import Generator
from uuid import uuid4

from llama_index.core import Settings
from llama_index.core.prompts import PromptTemplate
from llama_index.llms.openai import OpenAI as LlamaOpenAI
from openai import OpenAI

from ii.schema.enums import StoryLength
from ii.schema.story import StorySegment, StoryBlock, StoryInitiationRequest, Story, BlockImage


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

This will be the last STORYBLOCK? {last_block}. If YES, wrap up the story in the next block (do not provide any choices). 
"""

INITIAL_IMAGE_TEMPLATE = """
Generate an image based on the below plot scene. Choose an artistic style of any type but make sure to depict the setting, 
characters, and what they are doing. Do NOT include text in the generated image.

{story}
"""

IMAGE_TEMPLATE = """
Generate an image for a story based on the plot scene below. This image is not the first in the story and so the art style and 
imagery should be as close to the previous image as possible. Do NOT include text in the generated image.

===
Previous styles: {previous_styles}

===
Previous descriptions: {previous_descriptions}

===
{current_scene_description}
"""

IMAGE_DESCRIPTION_TEMPLATE = """
You are tasked with describing the image below. Give a description of the image and describe its artistic style. 
Make sure to accurately describe the setting, characters, and what they are doing.

If a main character is in the image then be sure to fully describe what they look like.

Also, be sure to be as descriptive as possible with the artistic style -- make it so that a future artist could create a similar image with the exact same description.

It was created with the story content: {story}. Image URL: {image_url}
"""


class OpenAIStoryteller:
    def __init__(self):
        self.llama_llm = LlamaOpenAI(model="gpt-4o", temperature=0.9)
        Settings.llm = self.llama_llm

        self.llm = OpenAI()

    def initiate_story(self, request: StoryInitiationRequest) -> None:
        prompt_template = PromptTemplate(SEGMENT_GENERATION_TEMPLATE)
        segment = self.llama_llm.structured_predict(
            StorySegment,
            prompt_template,
            story="",
            story_length=StoryLength.num_exchanges(request.length.value),
            num_blocks=0,
            genre=request.genre.value,
            last_block="NO",
        )

        image_resp = self.llm.images.generate(
            model="dall-e-3",
            prompt=INITIAL_IMAGE_TEMPLATE.format(story=segment.content),
            size="1024x1024",
            quality="standard",
            n=1
        )
        image_url = image_resp.data[0].url

        block_image = self.llama_llm.structured_predict(
            BlockImage,
            PromptTemplate(IMAGE_DESCRIPTION_TEMPLATE),
            story=segment.content,
            image_url=image_url,
        )

        return Story(
            id_=str(uuid4()),
            blocks=[StoryBlock(segment=segment, block_image=block_image)],
            genre=request.genre,
            length=request.length,
        )
    
    def continue_story(self, story: Story) -> Story:
        story_str = "\n".join(str(b) for b in story.blocks)
        last_block = "YES" if len(story.blocks) >= StoryLength.num_exchanges(story.length) else "NO"

        prompt_template = PromptTemplate(SEGMENT_GENERATION_TEMPLATE)
        segment = self.llama_llm.structured_predict(
            StorySegment,
            prompt_template,
            story=story_str,
            story_length=StoryLength.num_exchanges(story.length.value),
            num_blocks=len(story.blocks),
            genre=story.genre.value,
            last_block=last_block,
        )

        block_image = None    
        if last_block == "YES" or len(story.blocks) % 4 == 0:
            image_resp = self.llm.images.generate(
                model="dall-e-3",
                prompt=IMAGE_TEMPLATE.format(
                    previous_styles="\n ".join(b.block_image.image_style for b in story.blocks if b.block_image),
                    previous_descriptions="\n ".join(b.block_image.image_description for b in story.blocks if b.block_image),
                    current_scene_description=segment.content,
                ),
                size="1024x1024",
                quality="standard",
                n=1
            )
            image_url = image_resp.data[0].url

            block_image = self.llama_llm.structured_predict(
                BlockImage,
                PromptTemplate(IMAGE_DESCRIPTION_TEMPLATE),
                story=segment.content,
                image_url=image_url,
            )

        return Story(
            id_=story.id_,
            blocks=story.blocks + [StoryBlock(segment=segment, block_image=block_image)],
            genre=story.genre,
            length=story.length,
        )


storyteller = OpenAIStoryteller()


def yield_storyteller() -> Generator[OpenAIStoryteller, None, None]:
    yield storyteller
