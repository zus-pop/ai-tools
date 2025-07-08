from pydantic import BaseModel

class IsNSFW(BaseModel):
    is_safe: bool
    reason: str