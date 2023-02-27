#!/bin/sh

openssl req -x509 -nodes -newkey rsa:2048 -keyout key.pem -out cert.pem -sha256 -days 365 \
    -subj "/C=TR/ST=Eskisehir/L=None/O=None/OU=Telegram Bot/CN=quotes-bot"

docker compose -f docker-compose_self_ssl.yml up -d