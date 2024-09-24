from prometheus_client import Info, Gauge

from src.Model.Ping import Ping as PingModel
from src.Model.TraceRoute import TraceRoute as TraceRouteModel

labels = ["ip"]


class ConnectivityMetrics:
    __ping_loss = Gauge("ping_loss", "Ping loss percentage in scale 0.0 - 100.0", labels)
    __ping_latency_min = Gauge("ping_min_latency", "Min value of ping latency", labels)
    __ping_latency_max = Gauge("ping_max_latency", "Max value of ping latency", labels)
    __ping_latency_avg = Gauge("ping_avg_latency", "Avg value of ping latency", labels)

    __hops_count = Gauge("tracert_hops_count", "Traceroute hops count", labels)

    @staticmethod
    def update_metrics(pings: list[PingModel], traceroutes: list[TraceRouteModel]):
        ConnectivityMetrics.__update_ping_metrics(pings)
        ConnectivityMetrics.__update_traceroute_metrics(traceroutes)

    @staticmethod
    def __update_ping_metrics(pings: list[PingModel]):
        for ping in pings:
            ConnectivityMetrics.__ping_loss.labels(**{"ip": ping.ip}).set(ping.loss)
            ConnectivityMetrics.__ping_latency_min.labels(**{"ip": ping.ip}).set(ping.latency_min)
            ConnectivityMetrics.__ping_latency_max.labels(**{"ip": ping.ip}).set(ping.latency_max)
            ConnectivityMetrics.__ping_latency_avg.labels(**{"ip": ping.ip}).set(ping.latency_avg)

    @staticmethod
    def __update_traceroute_metrics(traceroutes: list[TraceRouteModel]):
        for tracert in traceroutes:
            ConnectivityMetrics.__hops_count.labels(**{"ip":tracert.ip}).set(tracert.hops_count)