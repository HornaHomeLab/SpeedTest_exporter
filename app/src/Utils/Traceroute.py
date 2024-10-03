import subprocess
from src.Model.TraceRoute import TraceRoute as TraceRouteModel
import src.Config as Config
from src.Observability import *

tracer = trace.get_tracer("Utils/TraceRoute")


class TraceRoute:
    __cmd_name: str = "traceroute"
    __cmd_timeout: int = Config.TRACEROUTE_TIMEOUT

    @staticmethod
    @tracer.start_as_current_span("TraceRoute.run")
    def run(ip: str) -> TraceRouteModel:

        span = get_current_span()
        span.set_attribute("ip_to_test",ip)
        error: bool = False

        result_data: dict[str, float] = {"ip": ip}
        cmd_to_run = TraceRoute.__get_cmd(ip)

        logger.info(
            "Executing TraceRoute command",
            extra={
                "cmd_to_run": cmd_to_run,
                "ip_to_test": ip
            }
        )

        try:
            out: list[str] = (
                subprocess.check_output(
                    cmd_to_run,
                    timeout=TraceRoute.__cmd_timeout,
                    stderr=subprocess.PIPE  # to suppress unnecessary traceroute prints
                )
                .decode('utf-8')
                .split("\n")
            )
            result_data["hops_count"] = TraceRoute.__get_hops_number(out)
        except Exception as e:
            error = True
            logger.exception(e, exc_info=True)

        result = TraceRouteModel(
            **result_data
        )
        set_current_span_status(error)
        return result

    @staticmethod
    def __get_cmd(ip: str):
        return [TraceRoute.__cmd_name, ip]

    @staticmethod
    def __get_hops_number(output: list[str]) -> int:
        reverse_line_counter: int = 2

        hops = ""
        while (hops == ""):
            result = output[len(output) - reverse_line_counter]
            hops = result.split(" ")[1]
            reverse_line_counter = reverse_line_counter + 1

        return int(hops)
