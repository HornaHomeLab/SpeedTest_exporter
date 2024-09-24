from fastapi import APIRouter, Response
from prometheus_client import generate_latest


Prometheus = APIRouter()


@Prometheus.get(path="/metrics")
def get_metrics():
    return Response(
        content=generate_latest(),
        media_type="text/plain"
    )
