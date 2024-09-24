from fastapi import APIRouter, Response
import src.Controller as Controller
import src.Model as Model


SpeedTest = APIRouter()


@SpeedTest.post("/SpeedTest", response_model=Model.SpeedTest)
def run_speedtest_on_demand():
    '''
        Endpoint to manually execute speedtest when needed.
        This action will update exposed Prometheus metrics.
    '''
    return (
        Controller.SpeedTest.perform_speed_test()
    )
