from llama_index.core.llms import MessageRole
from pydantic import BaseModel
 

class Choice(BaseModel):
   index: int
   content: str
   chosen: bool = False


class ChatMessage(BaseModel):
    role: MessageRole
    content: str
    choices: list[Choice] | None = None
