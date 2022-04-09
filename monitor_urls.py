import prometheus_client
import time
import requests
import os
import json
import validators
import logging
import unittest

# read env vars:
#  - URL_LIST to get the URLs for monitoring
#  - M_PORT - port used to expose the metrics
#  - UPDATE_PERIOD - poll interval in seconds
url_list = json.loads(os.environ['URL_LIST'])
m_port = int(os.environ['M_PORT'])
UPDATE_PERIOD = int(os.environ['UPDATE_PERIOD'])
# Prometheus gauges
SYSTEM_USAGE_UP = prometheus_client.Gauge('sample_external_url_up',
                                          'Shows URL status based on http status code 200',
                                          ['url'])
SYSTEM_USAGE_MS = prometheus_client.Gauge('sample_external_url_response_ms',
                                          'URL response time in milliseconds',
                                          ['url'])


# poll the URLs and set the gouges
def url_check(url_to_check):
    if not validators.url(url_to_check):
        logging.error("Not valid URL: " + url_to_check)
        return 1
    else:
        resp = requests.get(url_to_check)
        resp_dict = {"status_code": 1 if resp.status_code == 200 else 0,
                     "response_milliseconds": round(resp.elapsed.microseconds / 1000)}
        logging.info("URL " + url_to_check + " check result: ", resp_dict)
        SYSTEM_USAGE_UP.labels(url_to_check).set(resp_dict["status_code"])
        SYSTEM_USAGE_MS.labels(url_to_check).set(resp_dict["response_milliseconds"])
        return 0


# unittest
class TestUrlCheck(unittest.TestCase):
    def test_url_check(self):
        before_up = prometheus_client.REGISTRY.get_sample_value(SYSTEM_USAGE_UP)
        before_ms = prometheus_client.REGISTRY.get_sample_value(SYSTEM_USAGE_MS)
        url_check(url_list[0])
        after_up = prometheus_client.REGISTRY.get_sample_value(SYSTEM_USAGE_UP)
        after_ms = prometheus_client.REGISTRY.get_sample_value(SYSTEM_USAGE_MS)
        self.assertEqual(after_up, before_up)
        self.assertEqual(after_ms, before_ms)


if __name__ == '__main__':
    try:
        prometheus_client.start_http_server(m_port)
        logging.info("Prometheus client is started")
    except BaseException as err:
        logging.error(f"During Prometheus client starting - Unexpected {err=}, {type(err)=}")

while True:
    for m_url in url_list:
        url_check(m_url)
    time.sleep(UPDATE_PERIOD)
