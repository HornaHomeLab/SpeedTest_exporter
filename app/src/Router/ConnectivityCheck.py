from fastapi import APIRouter, Response, HTTPException
from prometheus_client import generate_latest
import src.Controller as Controller
import src.Model as Model
from src.Observability import *

ConnectivityCheck = APIRouter()


@ConnectivityCheck.post("/ConnectivityCheck", response_model=Model.ConnectivityCheck)
def run_connectivity_check():
    '''
        Endpoint to manually execute ConnectivityCheck (ping and traceroute) when needed.
        This action will update exposed Prometheus metrics.
    '''
    get_current_span()
    headers = get_response_headers()
    logger.info("ConnectivityCheck on demand called")
    
    try:
        check = Controller.InternetAccess.perform_connectivity_check()
        response = Response(
            check.model_dump_json(indent=4),
            headers=headers
        )
    except Exception as e:
        logger.exception(e,exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=headers,
            headers=headers
        )
    else:
        set_current_span_status()
        return response
    
@ConnectivityCheck.get("/Ping", response_model=Model.Ping)
def run_ping(ip_addresses: str):
    '''
        Endpoint to manually execute ping command to provided IP address.
    '''
    get_current_span()
    headers = get_response_headers()
    try:
        check = Controller.InternetAccess.ping([ip_addresses])[0]
        response = Response(
            check.model_dump_json(indent=4),
            headers=headers
        )
    except Exception as e:
        logger.exception(e,exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=headers,
            headers=headers
        )
    else:
        set_current_span_status()
        return response
    
@ConnectivityCheck.get("/Tracert", response_model=Model.TraceRoute)
def run_tracert(ip_addresses: str):
    '''
        Endpoint to manually execute traceroute to provided IP address.
    '''
    get_current_span()
    headers = get_response_headers()
    try:
        check = Controller.InternetAccess.traceroute([ip_addresses])[0]
        response = Response(
            check.model_dump_json(indent=4),
            headers=headers
        )
    except Exception as e:
        logger.exception(e,exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=headers,
            headers=headers
        )
    else:
        set_current_span_status()
        return response