from fastapi import APIRouter, Depends

from ii.clients.openai_storyteller import OpenAIStoryteller, yield_storyteller
from ii.schema.story import StoryInitiationRequest, Story


router = APIRouter(
    prefix="/story",
    tags=["story"],
)


@router.post("/initiate")
async def initiate_story(
    request: StoryInitiationRequest,
    storyteller: OpenAIStoryteller = Depends(yield_storyteller),
) -> Story:

    return storyteller.initiate_story(request)

@router.post("/continue")
async def continue_story(
    request: Story,
    storyteller: OpenAIStoryteller = Depends(yield_storyteller),
) -> Story:

    return storyteller.continue_story(request)
