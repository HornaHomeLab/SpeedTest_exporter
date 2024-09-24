from fastapi import APIRouter, Response
from prometheus_client import generate_latest
import src.Controller as Controller
import src.Model as Model

ConnectivityCheck = APIRouter()


@ConnectivityCheck.post("/ConnectivityCheck", response_model=Model.ConnectivityCheck)
def run_connectivity_check():
    '''
        Endpoint to manually execute ConnectivityCheck (ping and traceroute) when needed.
        This action will update exposed Prometheus metrics.
    '''
    return (
        Controller.InternetAccess.perform_connectivity_check()
    )
    
@ConnectivityCheck.get("/Ping", response_model=Model.Ping)
def run_ping(ip_addresses: str):
    '''
        Endpoint to manually execute ping command to provided IP address.
    '''
    return (
        Controller.InternetAccess.ping([ip_addresses])
    )
    
@ConnectivityCheck.get("/Tracert", response_model=Model.TraceRoute)
def run_tracert(ip_addresses: str):
    '''
        Endpoint to manually execute traceroute to provided IP address.
    '''
    return (
        Controller.InternetAccess.traceroute([ip_addresses])
    )