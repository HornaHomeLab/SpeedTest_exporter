# Utils

## Prometheus metrics
Definition of Prometheus metrics exposed on default /metrics endpoint. Provides `.update_metrics()` method to update all metrics based on passed [SpeedTest](/app/src/Model/SpeedTest/SpeedTest.py) object.

## SpeedTest by Ookla
Uses [Speedtest CLI](https://www.speedtest.net/apps/cli) app installed in docker container
to perform Internet speed test and return results as [SpeedTest](/app/src/Model/SpeedTest/SpeedTest.py) object.