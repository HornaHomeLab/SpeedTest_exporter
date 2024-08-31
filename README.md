<p float="left">
  <img src="/Pictures/prometheus_logo.png" height="100" />
  <img src="/Pictures/speedtest_by_ookla_logo.png" height="100" />
  <img src="/Pictures/fastapi_logo.png" height="100" />
  <img src="/Pictures/docker_logo.png" height="100" />
</p>

# Internet_SpeedTest_exporter
##### version: 0.0.1

Prometheus Exporter for speedTest by Ookla.

It is containerized FastAPI based application to periodically perform internet SpeedTest and expose results for Prometheus Server to scrape.

Speedtests are performed in the background based on specified in `.env` frequency.
Last speedtest result is available on `./metrics` endpoint. 
If program could not perform a test it will set all numeric values to 0 and string values to `-`

## Grafana Dashboard
![image](/Grafana/Pictures/Grafana_dashboard.png)

## Getting started
Review values in `.env` file and set it according to your needs.
1. `docker compose build` to build docker image
2. `docker compose up -d` to start docker container

