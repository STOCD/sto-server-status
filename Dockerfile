FROM python:3-slim

RUN mkdir -p /opt/
RUN mkdir -p /opt/data/

COPY requirements.txt /tmp/
COPY status.py /opt/

RUN python3 -m pip install -r /tmp/requirements.txt
RUN rm /tmp/requirements.txt

WORKDIR /opt/data
ENTRYPOINT [ "python3", "/opt/status.py" ]
