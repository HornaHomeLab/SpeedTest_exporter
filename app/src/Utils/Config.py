import os
import json
from dotenv import load_dotenv

load_dotenv()


class Config:

    __connectivity_check_servers: list[str] = ["1.1.1.1", "8.8.8.8", "8.8.4.4"]
    
    __intervals: dict[str, int] = {
        "SPEEDTEST": 1800,
        "CONNECTIVITY": 15
    }
    __timeouts: dict[str, int] = {
        "PING": 15,
        "TRACEROUTE": 15
    }

    @staticmethod
    def get_connectivity_servers() -> list[str]:
        try:
            servers = json.loads(
                os.getenv("CONNECTIVITY_CHECK_SERVERS", "[]")
            )
        except Exception as e:
            print(e)
            servers = Config.__connectivity_check_servers

        return servers
    
    @staticmethod
    def get_action_interval(name: str) -> int:
        name = name.upper()
        
        return int(
            os.getenv(
                "{action_name}_INTERVAL".format(
                    action_name=name),
                Config.__intervals[name]
            )
        )
    
    @staticmethod
    def get_subprocess_timeout(name: str) -> int:
        name = name.upper()
        return int(
            os.getenv(
                "{subprocess_name}_TIMEOUT".format(
                    subprocess_name=name),
                Config.__timeouts[name]
            )
        )