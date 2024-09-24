import subprocess
import os
from src.Model.TraceRoute import TraceRoute as TraceRouteModel

class TraceRoute:
    __cmd_name: str = "traceroute"
    __cmd_timeout: int = 10
    
    @staticmethod
    def run(ip: str) -> TraceRouteModel:
        result: dict[str, float] = {"ip": ip}
        cmd_to_run = TraceRoute.__get_cmd(ip)
        try:
            out: list[str] = (
                subprocess.check_output(
                    cmd_to_run,
                    timeout=TraceRoute.__cmd_timeout,
                    stderr=subprocess.PIPE # to suppress unnecessary traceroute prints
                )
                .decode('utf-8')
                .split("\n")
            )
            result["hops_count"] = TraceRoute.__get_hops_number(out)
        except Exception as e:
            print(e)

        return TraceRouteModel(
            **result
        )
    
    @staticmethod
    def __get_cmd(ip: str):
        return [TraceRoute.__cmd_name, ip]
    
    @staticmethod
    def __get_hops_number(output: list[str]) -> int:
        reverse_line_counter: int = 2
        
        hops = ""
        while(hops == ""):
            result = output[len(output) -  reverse_line_counter]
            hops = result.split(" ")[1]
            reverse_line_counter = reverse_line_counter + 1
            
        return int(hops)