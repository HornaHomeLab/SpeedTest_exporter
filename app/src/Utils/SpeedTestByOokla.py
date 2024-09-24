from src.Model.SpeedTest import SpeedTest

import shutil
import subprocess
import json


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
    def run_speedtest() -> SpeedTest:
        try:
            out_raw: bytes = SpeedTestByOokla.__run_ookla_subprocess()
            parsed_json: dict = SpeedTestByOokla.__parse_json_output(out_raw)
            
        except Exception:
            return SpeedTest()

        return SpeedTest(**parsed_json)

    @staticmethod
    def __parse_json_output(data: bytes) -> dict:
        try:
            parsed_json = json.loads(data)
        except Exception:
            raise Exception("Speedtest output is corrupted")
        return parsed_json

    @staticmethod
    def __run_ookla_subprocess() -> bytes:
        cmd_to_run = SpeedTestByOokla.__build_cmd_to_run()
        try:
            out = subprocess.check_output(
                cmd_to_run,
                timeout=SpeedTestByOokla.__test_timeout_seconds
            )
        except subprocess.CalledProcessError as e:
            raise Exception(e.output)
        except subprocess.TimeoutExpired as e:
            raise Exception("Execution took longer than expected")

        return out
    
    @staticmethod
    def __build_cmd_to_run() -> list[str]:
        return (
            [SpeedTestByOokla.__package_name] + SpeedTestByOokla.__cmd_args
        )
