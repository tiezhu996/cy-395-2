from pydantic import BaseModel


class RegisterRequest(BaseModel):
    name: str


class ApiKeyResponse(BaseModel):
    name: str
    api_key: str
