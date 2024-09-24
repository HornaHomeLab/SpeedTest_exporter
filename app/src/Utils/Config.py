import os
import json
from dotenv import load_dotenv

load_dotenv()


class Config:

    __connectivity_check_servers: list[str] = ["1.1.1.1", "8.8.8.8", "8.8.4.4"]
    __speed_test_interval: int = 30
    __connectivity_interval: int = 15

    @staticmethod
    def get_speedtest_interval() -> int:
        return int(
            60 * int(os.getenv(
                "SPEED_TEST_INTERVAL_MINUTES",
                Config.__speed_test_interval
            ))
        )

    @staticmethod
    def get_connectivity_interval() -> int:
        return int(
            os.getenv(
                "CONNECTIVITY_CHECK_INTERVAL_SECONDS",
                Config.__connectivity_interval
            )
        )

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
