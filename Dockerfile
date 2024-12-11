FROM debian:bookworm
WORKDIR /src

RUN apt-get update && \
    apt-get install -y python3-full && \
    python3 -m venv /src && \
    bin/pip install paho-mqtt python-dotenv ruff
ENV PATH="/src/bin:$PATH"

ADD . /src

CMD python mqtt_bt_status.py
