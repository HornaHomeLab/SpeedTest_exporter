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
        return int(
            Config.__get_env_value(name,"interval", Config.__intervals)
        )

    @staticmethod
    def get_subprocess_timeout(name: str) -> int:
        return int(
            Config.__get_env_value(name, "timeout", Config.__timeouts)
        )

    def __get_env_value(value_name: str, value_suffix: str, default_values: dict[str, int]):
        value_name = value_name.upper()
        value_suffix = value_suffix.upper()

        value_to_return =  os.getenv(
            "{name}_{suffix}".format(
                name=value_name,
                suffix=value_suffix
            ),
            default_values.get(value_name, None)
        )

        if value_to_return is None:
            raise Exception(f"{value_name} is not defined")
        
        return value_to_return