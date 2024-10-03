import threading
from src.Utils.Ping import Ping
from src.Model.Ping import Ping as PingModel
from src.Utils.Traceroute import TraceRoute
from src.Model.TraceRoute import TraceRoute as TraceRouteModel
from src.Prometheus.ConnectivityMetrics import ConnectivityMetrics
from src.Model.ConnectivityCheck import ConnectivityCheck
import src.Config as Config
from src.Observability import *

tracer = trace.get_tracer("Controller/InternetAccess")


class InternetAccess:

    @staticmethod
    @tracer.start_as_current_span("InternetAccess.perform_connectivity_check")
    def perform_connectivity_check() -> ConnectivityCheck:

        get_current_span()

        traceroutes: list[TraceRouteModel] = InternetAccess.traceroute()
        pings: list[PingModel] = InternetAccess.ping()

        ConnectivityMetrics.update_metrics(pings, traceroutes)

        result = ConnectivityCheck(
            **{
                "Pings": pings,
                "TraceRoutes": traceroutes
            }
        )

        set_current_span_status()

        return result

    @staticmethod
    @tracer.start_as_current_span("InternetAccess.ping")
    def ping(servers: list[str] = Config.CONNECTIVITY_SERVERS) -> list[PingModel]:

        ping_threads: list[threading.Thread] = []
        tests: list[PingModel] = []
        otel_context = context.get_current()
        logger.info(
            "Ping method called",
            extra={
                "servers_to_check": servers
            }
        )

        @tracer.start_as_current_span("__ping_thread", context=otel_context)
        def __ping_thread(ip: str):
            span = get_current_span()
            span.set_attribute("ip_to_test", ip)
            tests.append(
                Ping.run(ip)
            )
            set_current_span_status()

        for ip in servers:
            ping_threads.append(
                threading.Thread(target=__ping_thread, args=(ip,))
            )
            ping_threads[-1].start()
            logger.info(
                "Ping for {ip} started.".format(
                    ip=ip
                )
            )

        for thread in ping_threads:
            thread.join()

        set_current_span_status()
        return tests

    @staticmethod
    @tracer.start_as_current_span("InternetAccess.traceroute")
    def traceroute(servers: list[str] = Config.CONNECTIVITY_SERVERS) -> list[TraceRouteModel]:

        tracert_threads: list[threading.Thread] = []
        tests: list[TraceRouteModel] = []
        otel_context = context.get_current()
        logger.info(
            "Traceroute method called",
            extra={
                "servers_to_check": servers
            }
        )

        @tracer.start_as_current_span("__tracert_thread", context=otel_context)
        def __tracert_thread(ip: str):
            span = get_current_span()
            span.set_attribute("ip_to_test", ip)
            tests.append(
                TraceRoute.run(ip)
            )
            set_current_span_status()

        for ip in servers:
            tracert_threads.append(
                threading.Thread(target=__tracert_thread, args=(ip,))
            )
            tracert_threads[-1].start()
            logger.info(
                "Tracert for {ip} started.".format(
                    ip=ip
                )
            )

        for thread in tracert_threads:
            thread.join()

        set_current_span_status()
        return tests
