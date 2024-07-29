import os
from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi_utils.tasks import repeat_every
from prometheus_client import make_asgi_app

import src.Controller as Controller
import src.Model as Model

metrics_app = make_asgi_app()

refresh_interval_period = 60 * int(os.getenv('SPEED_TEST_INTERVAL_MINUTES', 5))

print("Refresh interval is set to: ", refresh_interval_period, " seconds.")


@repeat_every(seconds=refresh_interval_period)
def perform_speed_test():
    Controller.SpeedTest.perform_speed_test()
    print("test performed")


@asynccontextmanager
async def app_lifespan(app: FastAPI):
    Controller.SpeedTest.check_components()
    await perform_speed_test()
    yield
    print("Closing app")

app = FastAPI(lifespan=app_lifespan)

app.mount("/metrics", metrics_app)


@app.post("/runOnDemand", response_model=Model.SpeedTest)
def run_speedtest_on_demand():
    '''
        Endpoint to manually execute speedtest when needed.
    '''
    return (
        Controller.SpeedTest.perform_speed_test()
    )


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host=os.getenv('INTERFACE_IP'),
                port=int(os.getenv('API_PORT')))
