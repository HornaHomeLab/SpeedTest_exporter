import os
import threading
from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi_utils.tasks import repeat_every
from src.Utils.Config import Config
import src.Controller as Controller
import src.Router as Router

lock = threading.Lock()


@repeat_every(seconds=Config.get_action_interval("SPEEDTEST"))
def perform_speed_test():
    lock.acquire()
    try:
        Controller.SpeedTest.perform_speed_test()
        print("Speedtest performed")
    finally:
        lock.release()


@repeat_every(seconds=Config.get_action_interval("CONNECTIVITY"))
def perform_ping_and_tracert():
    lock.acquire()
    try:
        Controller.InternetAccess.perform_connectivity_check()
        print("Connectivity check performed")
    finally:
        lock.release()


@asynccontextmanager
async def app_lifespan(app: FastAPI):
    Controller.SpeedTest.check_components()
    await perform_speed_test()
    await perform_ping_and_tracert()
    yield
    print("Closing app")

app = FastAPI(lifespan=app_lifespan)
app.include_router(Router.SpeedTest)
app.include_router(Router.Prometheus)
app.include_router(Router.ConnectivityCheck)


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port="8000")
