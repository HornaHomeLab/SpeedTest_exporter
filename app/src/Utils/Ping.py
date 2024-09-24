import subprocess
from src.Model.Ping import Ping as PingModel


class Ping:

    __cmd_name: str = "ping"
    __cmd_args: list[str] = ["-c", "8"]
    __cmd_timeout: int = 10

    @staticmethod
    def run(ip: str) -> PingModel:
        result: dict[str, float] = {"ip": ip}
        cmd_to_run = Ping.__get_cmd(ip)
        try:
            out: list[str] = (
                subprocess.check_output(
                    cmd_to_run,
                    timeout=Ping.__cmd_timeout
                )
                .decode('utf-8')
                .split("\n")
            )
            
            result["loss"] = Ping.__get_packet_loss(out)
            result["latency_min"], result["latency_avg"], result["latency_max"] = Ping.__get_latency(out)
        except Exception as e:
            print(e)
        response = PingModel(
            **result
        )
        return response

    @staticmethod
    def __get_cmd(ip: str):
        return [Ping.__cmd_name, ip] + Ping.__cmd_args

    @staticmethod
    def __get_packet_loss(output: list[str]) -> float:
        result = output[len(output) - 3]
        loss_line = result.split(",")[2]
        loss = loss_line.split("%")[0]
        return float(loss)

    @staticmethod
    def __get_latency(output: list[str]) -> tuple[float, float, float]:
        result = output[len(output) - 2]
        numbers = result.split("=")[1].split("/")
        return (
            float(numbers[0]),
            float(numbers[1]),
            float(numbers[2])
        )
