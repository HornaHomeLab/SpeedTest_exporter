# SpeedTest exporter
FastAPI based application performs internet speed tests at regular intervals (specified in `.env` file).
After each speedtest Prometheus metrics are automatically updated with the latest results.

## How It Works
1. Scheduled Speed Tests:
    - The speed test is performed at intervals defined by the SPEED_TEST_INTERVAL_MINUTES environment variable.
    - The interval is managed using FastAPI Utils’ repeat_every decorator.
2. On-Demand Speed Tests:
    - The `/runOnDemand endpoint` allows users to trigger a speed test on-demand. 
    The result of the speed test is returned in the response.
3. Metrics:
    - Metrics are collected via Prometheus’ make_asgi_app and served at the `/metrics` endpoint.
    - These metrics can be scraped by Prometheus for monitoring and alerting.