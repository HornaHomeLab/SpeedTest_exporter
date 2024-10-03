import threading
from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi_utils.tasks import repeat_every
import src.Controller as Controller
import src.Router as Router
import src.Config as Config
from src.Observability import *

lock = threading.Lock()

tracer = trace.get_tracer("Main/Scheduled_Jobs")


@repeat_every(seconds=Config.SPEEDTEST_INTERVAL)
@tracer.start_as_current_span("perform_speed_test")
def perform_speed_test():
    lock.acquire()
    try:
        Controller.SpeedTest.perform_speed_test()
    except Exception as e:
        logger.exception(e, exc_info=True)
    else:
        logger.info("SpeedTest performed successfully")
    finally:
        lock.release()


@repeat_every(seconds=Config.CONNECTIVITY_INTERVAL)
@tracer.start_as_current_span("perform_ping_and_tracert")
def perform_ping_and_tracert():
    lock.acquire()
    try:
        Controller.InternetAccess.perform_connectivity_check()
    except Exception as e:
        logger.exception(e, exc_info=True)
    else:
        logger.info("Ping and Tracert performed successfully")
    finally:
        lock.release()


@asynccontextmanager
async def app_lifespan(app: FastAPI):
    logger.info(
        """Starting {svc}
        SpeedTest interval: {st_int} seconds
        Connectivity Check interval: {cc_int} seconds""".format(
            svc=Config.SERVICE_NAME,
            st_int=Config.SPEEDTEST_INTERVAL,
            cc_int=Config.CONNECTIVITY_INTERVAL
        )
    )
    Controller.SpeedTest.check_components()
    await perform_speed_test()
    await perform_ping_and_tracert()
    yield
    logger.info(f"Stopping {Config.SERVICE_NAME}")

app = FastAPI(lifespan=app_lifespan)
app.include_router(Router.SpeedTest)
app.include_router(Router.Prometheus)
app.include_router(Router.ConnectivityCheck)

opentelemetry_instrument(app)
prometheus_instrument(app)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port="8000")
