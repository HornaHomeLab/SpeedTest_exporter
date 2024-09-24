from pydantic import BaseModel, Field


class Ping(BaseModel):
    ip: str
    loss: float = Field(default=100.0)
    latency_min: float = Field(default=0.0)
    latency_avg: float = Field(default=0.0)
    latency_max: float = Field(default=0.0)