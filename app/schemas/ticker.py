from pydantic import BaseModel


class TickerResponse(BaseModel):
    name: str
    description: str
    icon_url: str | None
