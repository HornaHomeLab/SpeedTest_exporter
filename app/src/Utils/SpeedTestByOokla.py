import shutil
import subprocess
import json
from src.Model.SpeedTest import SpeedTest
from src.Observability import *

tracer = trace.get_tracer("Utils/SpeedTestByOokla")


class SpeedTestByOokla:

    __package_name = "speedtest"
    __test_timeout_seconds = 120

    __cmd_args = [
        "--format=json",
        "--progress=no",
        "--accept-license",
        "--accept-gdpr"
    ]

    @staticmethod
    def check_if_speedtest_package_exist():
        if shutil.which(SpeedTestByOokla.__package_name) is None:
            raise Exception(
                "Can not find package {package} in the system".format(
                    package=SpeedTestByOokla.__package_name
                )
            )

    @staticmethod
    @tracer.start_as_current_span("run_speedtest")
    def run_speedtest() -> SpeedTest:
        get_current_span()

        out_raw: bytes = SpeedTestByOokla.__run_ookla_subprocess()
        parsed_json: dict = SpeedTestByOokla.__parse_json_output(out_raw)

        result = SpeedTest(**parsed_json)
        
        set_current_span_status()
        
        return result

    @staticmethod
    def __parse_json_output(data: bytes) -> dict:
        try:
            parsed_json = json.loads(data)
        except Exception:
            raise Exception("Speedtest output is corrupted")
        return parsed_json

    @staticmethod
    @tracer.start_as_current_span("run_ookla_subprocess")
    def __run_ookla_subprocess() -> bytes:
        get_current_span()
        error: bool = False
        cmd_to_run = SpeedTestByOokla.__build_cmd_to_run()
        try:
            out = subprocess.check_output(
                cmd_to_run,
                timeout=SpeedTestByOokla.__test_timeout_seconds
            )
        except subprocess.CalledProcessError as e:
            error=True
            logger.exception(e, exc_info=True)
            raise Exception(e.output)
        except subprocess.TimeoutExpired as e:
            error=True
            logger.exception(e, exc_info=True)
            raise Exception("Execution took longer than expected")

        set_current_span_status(error)
        return out

    @staticmethod
    def __build_cmd_to_run() -> list[str]:
        return (
            [SpeedTestByOokla.__package_name] + SpeedTestByOokla.__cmd_args
        )
