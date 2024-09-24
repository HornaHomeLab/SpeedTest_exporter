from pydantic import BaseModel, Field
from src.Model.Ping import Ping
from src.Model.TraceRoute import TraceRoute

class ConnectivityCheck(BaseModel):
    Pings: list[Ping]
    TraceRoutes: list[TraceRoute]