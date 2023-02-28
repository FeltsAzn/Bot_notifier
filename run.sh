#!/bin/sh

docker volume create --name=nginx_conf
docker volume create --name=letsencrypt_certs
docker compose -f docker-compose.yml up -d
docker compose logs -f