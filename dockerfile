FROM debian:bookworm
WORKDIR /src

RUN apt-get update && apt-get install -y python3-full && python3 -m venv /src && bin/pip install paho-mqtt python-dotenv

ADD . /src

CMD bash -c "source bin/activate && ./mqtt_bt_status.py"
