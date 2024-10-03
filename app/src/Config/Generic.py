import os
import json
from dotenv import load_dotenv

load_dotenv()

SERVICE_NAME = "SpeedTest_Exporter"
ENVIRONMENT = os.getenv("ENVIRONMENT_TYPE", "dev")

CONNECTIVITY_INTERVAL = int(os.getenv("CONNECTIVITY_INTERVAL", 15))
PING_TIMEOUT = int(os.getenv("PING_TIMEOUT", 15))
TRACEROUTE_TIMEOUT = int(os.getenv("TRACEROUTE_TIMEOUT", 15))
CONNECTIVITY_SERVERS: list[str] = json.loads(
    os.getenv(
        "CONNECTIVITY_CHECK_SERVERS",
        '["1.1.1.1", "8.8.8.8", "8.8.4.4"]'
    )
)


SPEEDTEST_INTERVAL = int(os.getenv("SPEEDTEST_INTERVAL", 1800))