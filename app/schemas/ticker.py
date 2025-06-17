from pydantic import BaseModel

class TickerResponse(BaseModel):
    id: int
    name: str
