from pydantic import BaseModel, Field


class SubscriptionCreate(BaseModel):
    base: str = Field(min_length=3, max_length=3)
    quote: str = Field(min_length=3, max_length=3)
    target_rate: float
    notify_url: str
    email: str = ""
