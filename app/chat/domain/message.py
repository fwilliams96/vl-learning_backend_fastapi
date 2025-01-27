from pydantic import BaseModel

class Metadata(BaseModel):
    soundFile: str
    duration: float

class MouthCue(BaseModel):
    start: float
    end: float
    value: str

class Lipsync(BaseModel):
    metadata: Metadata
    mouthCues: list[MouthCue]

class Message(BaseModel):
    text: str
    audio: str
    lipsync: Lipsync
    facialExpression: str
    animation: str

class Chat(BaseModel):
    id: str
    messages: list[Message]
    user_id: str



