from typing import Generator
from uuid import uuid4

from llama_index.core import Settings
from llama_index.core.prompts import PromptTemplate
from llama_index.llms.openai import OpenAI as LlamaOpenAI
from openai import OpenAI

from ii.schema.enums import StoryLength
from ii.schema.story import (
    StorySegment,
    StoryBlock,
    StoryInitiationRequest,
    Story,
    BlockImage,
)
from ii.clients.templates.llama_templates import (
    SEGMENT_GENERATION_TEMPLATE,
    INITIAL_IMAGE_TEMPLATE,
    IMAGE_DESCRIPTION_TEMPLATE,
    IMAGE_TEMPLATE,
)


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
            n=1,
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
        last_block = (
            "YES"
            if len(story.blocks) >= StoryLength.num_exchanges(story.length)
            else "NO"
        )

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
                    previous_styles="\n ".join(
                        b.block_image.image_style for b in story.blocks if b.block_image
                    ),
                    previous_descriptions="\n ".join(
                        b.block_image.image_description
                        for b in story.blocks
                        if b.block_image
                    ),
                    current_scene_description=segment.content,
                ),
                size="1024x1024",
                quality="standard",
                n=1,
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
            blocks=story.blocks
            + [StoryBlock(segment=segment, block_image=block_image)],
            genre=story.genre,
            length=story.length,
        )


storyteller = OpenAIStoryteller()


def yield_storyteller() -> Generator[OpenAIStoryteller, None, None]:
    yield storyteller
