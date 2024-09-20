from fastapi import APIRouter, Depends

from ii.clients.openai_storyteller import OpenAIStoryteller, yield_storyteller
from ii.schema.story_initiation import StoryInitiationRequest


router = APIRouter(
    prefix="/story",
    tags=["story"],
)


@router.post("/initiate")
async def initiate_story(
    request: StoryInitiationRequest,
    storyteller: OpenAIStoryteller = Depends(yield_storyteller)
) -> None:

    return storyteller.initiate_story(request)
