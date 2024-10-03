from prometheus_client import Gauge
from src.Prometheus.Registry import exporter_registry
from src.Model.Ping import Ping as PingModel
from src.Model.TraceRoute import TraceRoute as TraceRouteModel
from src.Observability import *

tracer = trace.get_tracer("Prometheus/ConnectivityMetrics")

labels = ["ip"]


class ConnectivityMetrics:
    __ping_loss = Gauge(
        "ping_loss", "Ping loss percentage in scale 0.0 - 100.0",
        labels, registry=exporter_registry
    )
    __ping_latency_min = Gauge(
        "ping_min_latency", "Min value of ping latency",
        labels, registry=exporter_registry
    )
    __ping_latency_max = Gauge(
        "ping_max_latency", "Max value of ping latency",
        labels, registry=exporter_registry
    )
    __ping_latency_avg = Gauge(
        "ping_avg_latency", "Avg value of ping latency",
        labels, registry=exporter_registry
    )
    __hops_count = Gauge(
        "tracert_hops_count", "Traceroute hops count",
        labels, registry=exporter_registry
    )

    @staticmethod
    @tracer.start_as_current_span("ConnectivityMetrics.update_metrics")
    def update_metrics(pings: list[PingModel], traceroutes: list[TraceRouteModel]):

        get_current_span()

        ConnectivityMetrics.__update_ping_metrics(pings)
        ConnectivityMetrics.__update_traceroute_metrics(traceroutes)

        logger.info(
            "Pings and trace routes metrics updated"
        )
        set_current_span_status()

    @staticmethod
    @tracer.start_as_current_span("ConnectivityMetrics.__update_ping_metrics")
    def __update_ping_metrics(pings: list[PingModel]):

        get_current_span()

        for ping in pings:
            ConnectivityMetrics.__ping_loss.labels(
                **{
                    "ip": ping.ip
                }
            ).set(ping.loss)
            ConnectivityMetrics.__ping_latency_min.labels(
                **{
                    "ip": ping.ip
                }
            ).set(ping.latency_min)
            ConnectivityMetrics.__ping_latency_max.labels(
                **{
                    "ip": ping.ip
                }
            ).set(ping.latency_max)
            ConnectivityMetrics.__ping_latency_avg.labels(
                **{
                    "ip": ping.ip
                }
            ).set(ping.latency_avg)

        logger.info(
            "Ping metrics updated for {num} tests.".format(
                num=len(pings)
            )
        )
        set_current_span_status()

    @staticmethod
    @tracer.start_as_current_span("ConnectivityMetrics.__update_traceroute_metrics")
    def __update_traceroute_metrics(traceroutes: list[TraceRouteModel]):

        get_current_span()

        for tracert in traceroutes:
            ConnectivityMetrics.__hops_count.labels(
                **{
                    "ip": tracert.ip
                }
            ).set(tracert.hops_count)

        logger.info(
            "Traceroute metrics updated for {num} tests.".format(
                num=len(traceroutes)
            )
        )

        set_current_span_status()
