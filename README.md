<p float="left">
  <img src="/Pictures/prometheus_logo.png" height="100" />
  <img src="/Pictures/speedtest_by_ookla_logo.png" height="100" />
  <img src="/Pictures/fastapi_logo.png" height="100" />
  <img src="/Pictures/docker_logo.png" height="100" />
</p>

# Internet_SpeedTest_exporter
[![CodeQL](https://github.com/HornaHomeLab/SpeedTest_exporter/actions/workflows/github-code-scanning/codeql/badge.svg)](https://github.com/HornaHomeLab/SpeedTest_exporter/actions/workflows/github-code-scanning/codeql)
[![CI/CD](https://github.com/HornaHomeLab/SpeedTest_exporter/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/HornaHomeLab/SpeedTest_exporter/actions/workflows/ci-cd.yml)

##### version: 2.0.2

Prometheus Exporter for speedTest by Ookla.

It is containerized FastAPI based application to periodically perform internet SpeedTest and expose results for Prometheus Server to scrape.

Speedtests are performed in the background based on specified in `.env` frequency.
Last speedtest result is available on `./metrics` endpoint. 
Additionally there is `/runOnDemand` to trigger speedtest execution on demand.
If program could not perform a test it will set all numeric values to 0 and string values to `-`

> [!IMPORTANT] 
> `/runOnDemand` endpoint can be used with `POST` method only.

## Grafana Dashboard
![image](/Grafana/Pictures/Grafana_dashboard.png)

## Getting started
Review values in `.env` file and set it according to your needs.
1. `docker compose build` to build docker image
2. `docker compose up -d` to start docker container

