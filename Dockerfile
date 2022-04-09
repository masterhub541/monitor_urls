FROM python:3.9-alpine
 
RUN mkdir -p /coding_assignment
WORKDIR /coding_assignment
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY monitor_urls.py .
ENV URL_LIST '["https://httpstat.us/503","https://httpstat.us/200"]'
ENV M_PORT 9999
ENV UPDATE_PERIOD 1

EXPOSE 9999

CMD python monitor_urls.py
