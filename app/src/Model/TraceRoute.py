from pydantic import BaseModel, Field


class TraceRoute(BaseModel):
    ip: str
    hops_count: int = Field(default=0)