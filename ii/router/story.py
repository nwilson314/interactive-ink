from fastapi import APIRouter, Depends

from ii.clients.openai_storyteller import OpenAIStoryteller, yield_storyteller
from ii.schema.story import StoryInitiationRequest, StoryInitiationResponse


router = APIRouter(
    prefix="/story",
    tags=["story"],
)


@router.post("/initiate")
async def initiate_story(
    request: StoryInitiationRequest,
    storyteller: OpenAIStoryteller = Depends(yield_storyteller),
) -> StoryInitiationResponse:

    return storyteller.initiate_story(request)
