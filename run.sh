#!/bin/bash

help() {
  echo "[HELP] -r REMOVE_IMAGES : remove selected docker images
       -s               : stop and remove docker containers
       -u               : start docker compose instruction"
}

delete_image() {
  # shellcheck disable=SC2162
  read -a images <<<"$*"

  for image_name in "${images[@]}"; do
    printf "[image] '%s' -> " "$image_name"
    docker rmi "$image_name"
  done

}

check_nginx_volume() {
  if ! docker volume ls -q | grep nginx_conf; then
    docker volume create --name=nginx_conf
    printf "[INFO] nginx_conf was volume created "
  fi
}

check_letsencrypt_volume() {
  if ! docker volume ls -q | grep letsencrypt_certs; then
    docker volume create --name=letsencrypt_certs
    printf "[INFO] letsencrypt_certs volume was created"
  fi
}

start() {
  check_nginx_volume
  check_letsencrypt_volume

  docker compose -f docker-compose.yml up -d
  docker compose logs -f
}

while getopts rdsh OPTION; do
  args_count="$#"
  case "$OPTION" in
  r)
    if [ $args_count -gt 1 ]; then
      shift
      delete_image "$*"
    else
      echo "[ERROR] You should write docker images names."
    fi
    ;;
  d)
    docker compose down
    echo "[INFO] docker compose stopped, container removed."
    ;;
  s)
    start
    ;;
  h)
    help
    ;;
  ?)
    echo "[ERROR] Wrong flag. Script usage: [-h help] [-r somevalues] [-s] [-u]"
    exit 1
    ;;
  esac
done
