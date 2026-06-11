from enum import Enum
from pydantic import BaseModel, Field


class Direction(str, Enum):
    both = "both"
    up = "up"
    down = "down"


class SubscriptionCreate(BaseModel):
    base: str = Field(min_length=3, max_length=3)
    quote: str = Field(min_length=3, max_length=3)
    target_rate: float
    direction: Direction = Direction.both
    notify_url: str
    email: str = ""


class SubscriptionResponse(BaseModel):
    id: int
    base: str
    quote: str
    target_rate: float
    direction: str
    notify_url: str
    email: str
    active: bool

    class Config:
        from_attributes = True
