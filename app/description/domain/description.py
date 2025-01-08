from enum import Enum
from typing import Optional
from pydantic import BaseModel

class DescriptionResult(BaseModel):
    solution: Optional[str] = None
    rating: float
    comments: Optional[str] = None

class Description(BaseModel):
    id: Optional[str] = None
    topic: str
    finished: bool = False
    image_url: Optional[str] = None
    image_id: str
    user_description: Optional[str] = None
    result: Optional[DescriptionResult] = None

class ImageDescription(BaseModel):
    id: Optional[str] = None
    topic: str
    url: str

class UserDescriptionFormat(Enum):
    TEXT = "text"
    AUDIO = "audio"

class UserDescription(BaseModel):
    format: UserDescriptionFormat
    content: str