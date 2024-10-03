from fastapi import APIRouter, Response, HTTPException
from prometheus_client import generate_latest
from src.Prometheus.Registry import exporter_registry, REGISTRY
from src.Observability import *

Prometheus = APIRouter()


def get_metrics_response(metrics_reg = REGISTRY) -> Response:
    get_current_span()
    response = Response(
        content=generate_latest(metrics_reg),
        media_type="text/plain",
        headers=get_response_headers()
    )
    set_current_span_status()
    return response

@Prometheus.get(path="/metrics")
def get_metrics():
    return get_metrics_response(exporter_registry)

@Prometheus.get(path="/appmetrics")
def get_metrics():
    return get_metrics_response()
