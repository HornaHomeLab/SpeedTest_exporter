import threading
from src.Utils.Ping import Ping
from src.Model.Ping import Ping as PingModel
from src.Utils.Traceroute import TraceRoute
from src.Model.TraceRoute import TraceRoute as TraceRouteModel
from src.Prometheus.ConnectivityMetrics import ConnectivityMetrics
from src.Model.ConnectivityCheck import ConnectivityCheck
from src.Utils.Config import Config


class InternetAccess:

    @staticmethod
    def perform_connectivity_check() -> ConnectivityCheck:
        traceroutes: list[TraceRouteModel] = InternetAccess.traceroute()
        pings: list[PingModel] = InternetAccess.ping()

        ConnectivityMetrics.update_metrics(pings, traceroutes)

        return ConnectivityCheck(
            **{
                "Pings": pings,
                "TraceRoutes": traceroutes
            }
        )

    @staticmethod
    def ping(servers: list[str] = Config.get_connectivity_servers()) -> list[PingModel]:
        ping_threads: list[threading.Thread] = []
        tests: list[PingModel] = []

        def __ping_thread(ip: str):
            tests.append(
                Ping.run(ip)
            )

        for ip in servers:
            ping_threads.append(
                threading.Thread(target=__ping_thread, args=(ip,))
            )
            ping_threads[-1].start()

        for thread in ping_threads:
            thread.join()

        return tests

    @staticmethod
    def traceroute(servers: list[str] = Config.get_connectivity_servers()) -> list[TraceRouteModel]:
        tracert_threads: list[threading.Thread] = []
        tests: list[TraceRouteModel] = []

        def __tracert_thread(ip: str):
            tests.append(
                TraceRoute.run(ip)
            )

        for ip in servers:
            tracert_threads.append(
                threading.Thread(target=__tracert_thread, args=(ip,))
            )
            tracert_threads[-1].start()

        for thread in tracert_threads:
            thread.join()

        return tests
