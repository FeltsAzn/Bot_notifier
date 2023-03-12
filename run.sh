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
    echo "[image] '%s' -> " "$image_name"
    docker rmi "$image_name"
  done

}

check_nginx_volume() {
  if ! docker volume ls -q | grep nginx_conf; then
    docker volume create --name=nginx_conf
    echo "[INFO] nginx_conf was volume created "
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

args_count="$#"
if [ $args_count == 0 ]; then
  echo "[INFO] Start docker compose..."
  start
else

  while getopts rdshia OPTION; do


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
      echo "[INFO] Docker compose stopped, containers removed."
      ;;
    a)
      docker rmi $(docker images -q)
      echo "[INFO] All docker images $pattern are deleted"
      ;;
    i)
      pattern=$2
      docker rmi $(docker images | grep $pattern)
      echo "[INFO] All docker images '$pattern' are deleted"
      ;;
    h)
      help
      ;;
    ?)
      echo "[ERROR] Wrong flag. Script usage: [-h help] [-r somevalues] [-d] [-s]"
      exit 1
      ;;
    *)

    esac
  done

fi