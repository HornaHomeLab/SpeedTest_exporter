from pydantic import BaseModel, Field

from src.Model.SpeedTestSubModels.Ping import NoWorkloadPing
from src.Model.SpeedTestSubModels.Transfer import Transfer
from src.Model.SpeedTestSubModels.Interface import Interface
from src.Model.SpeedTestSubModels.Server import Server
from src.Model.SpeedTestSubModels.Result import Result


class SpeedTest(BaseModel):
    _type: str
    timestamp: str
    ping: NoWorkloadPing = Field(default=NoWorkloadPing())
    download: Transfer = Field(default=Transfer())
    upload: Transfer = Field(default=Transfer())
    packet_loss: float = Field(alias='packetLoss', default=0.0)
    isp: str = Field(default="-")
    interface: Interface = Field(default=Interface())
    server: Server = Field(default=Server())
    result: Result = Field(default=Result())
