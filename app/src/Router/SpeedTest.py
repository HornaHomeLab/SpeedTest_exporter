from fastapi import APIRouter, Response, HTTPException
import src.Controller as Controller
import src.Model as Model
from src.Observability import *

SpeedTest = APIRouter()


@SpeedTest.post("/SpeedTest", response_model=Model.SpeedTest)
def run_speedtest_on_demand():
    '''
        Endpoint to manually execute speedtest when needed.
        This action will update exposed Prometheus metrics.
    '''
    get_current_span()
    logger.info("SpeedTest on demand called")
    
    headers = get_response_headers()
    try:
        speedtest: Model.SpeedTest = Controller.SpeedTest.perform_speed_test()
        
        response = Response(
            speedtest.model_dump_json(indent=4),
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
