# Internet_SpeedTest_exporter
##### version: 0.0.1

Containerized prometheus exporter for speedTest by Ookla.
All data available in speedtest cli are exposed for Prometheus to scrape.

Speedtests are performed in the background based on specified in `.env` frequency.
For prometheus scraper last speedtest result is available. 
If program could not perform a test it will set all numeric values to 0 and string values to `-`

## How to run it
Review values in `.env` file and set it according to your needs.

    docker compose up -d 

