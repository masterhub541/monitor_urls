# Monitor list of URLs service

The service is designed to monitor list of URLs and reports results as [Prometheus](https://https://prometheus.io/) metrics.

The service checks if the URLs are up based on HTTP status code 200 and response time in milliseconds.

#### Table Of Contents

1. [Quick start guide](#quick-start-guide)
2. [Features](#features)

## Quick Start Guide

Follow the steps below to run the service:

1. Download the code from [Git](https://github.com/masterhub541/monitor_urls)
2. Ensure you have [Docker](https://docs.docker.com/get-docker/) installed
3. Ensure you have [kubectl installed](https://kubernetes.io/docs/tasks/tools/) and access to k8s cluster
4. To run it in Docker:

   * Build the image `docker build -t <your_image_name> .`
   * Run the container `docker run -d -p 9999:9999 <your_image_name>`
   * Open browser and check `http://localhost:9999`
   * Optionally you can push the image in [docker hub](https://hub.docker.com/) for k8s usage later
5. To run it in k8s:

   * Use your image if you have such in docker hub otherwise you can use already pushed image [momodocker541/monitor_url](https://hub.docker.com/u/momodocker541)
   * Deploy using:
     * kubectl k8s/monitor_url.yaml file `kubectl apply -f monitor_urls.yaml`
     * Heml Chart in helm dir `helm install <your_app_name> monitor-url`
   * This will create k8s deployment, k8s service, k8s pod disruption budget
   * Check the app with `kubectl port-forward <your_pod_name> 8888:9999`
   * Open browser and check `http://localhost:8888`

## Features

1. The URLs for monitoring are in env variable URL_LIST
2. By default the service exposes metrics on HTTP port 9999, endpoint `/metrics`
3. The port can easily be changed through env variable M_PORT
4. Pool period is in UPDATE_PERIOD
5. Example:

   ```
   URL_LIST='["https://httpstat.us/503","https://httpstat.us/200"]'
   M_PORT=9999
   UPDATE_PERIOD=1
   ```
6. The variables can be managed through Dockerfile, `docker run -e...` or in k8s deployment YAML file
7. The metrics looks like:

   ```
   # HELP sample_external_url_up Shows URL status based on http status code 200
   # TYPE sample_external_url_up gauge
   sample_external_url_up{url="https://httpstat.us/503"} 0.0
   sample_external_url_up{url="https://httpstat.us/200"} 1.0
   # HELP sample_external_url_response_ms URL response time in milliseconds
   # TYPE sample_external_url_response_ms gauge
   sample_external_url_response_ms{url="https://httpstat.us/503"} 689.0
   sample_external_url_response_ms{url="https://httpstat.us/200"} 899.0
   ```
8. Once loaded in Prometheus the metrics can be used in Grafana dashboards:

[Prometheus target](https://github.com/masterhub541/monitor_urls/blob/main/pics/Prometheus_target.png)

[Prometheus metrics](https://github.com/masterhub541/monitor_urls/blob/main/pics/Prometheus_metrics.png)

[Grafana dashboard](https://github.com/masterhub541/monitor_urls/blob/main/pics/Grafana_dashboard.png)
