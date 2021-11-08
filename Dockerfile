FROM ubuntu:bionic
ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get -y install \
    python3 python3-dev python3-dev python3-pip python3-venv python3-wheel \
    libsqlclient-dev libssl-dev

ARG USER=root
USER $USER
RUN python3 -m venv venv
WORKDIR /app
COPY requirements.txt requirements.txt
RUN /venv/bin/pip install -r requirements.txt

COPY . /app
RUN mkdir -p /app/db/
EXPOSE 8000
RUN chmod +x /app/start.sh
ENTRYPOINT ["./start.sh"]
