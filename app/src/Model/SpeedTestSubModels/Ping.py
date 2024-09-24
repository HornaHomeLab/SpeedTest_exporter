from pydantic import BaseModel, Field


class Ping(BaseModel):
    jitter: float = Field(default=0.0)
    low: float = Field(default=0.0)
    high: float = Field(default=0.0)


class NoWorkloadPing(Ping):
    latency: float = Field(default=0.0)


class TransferPing(Ping):
    iqm: float = Field(default=0.0)
