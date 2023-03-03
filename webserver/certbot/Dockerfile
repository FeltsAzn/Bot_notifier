FROM certbot/certbot:v1.29.0
services:
  nginx:
    build: ./webserver/nginx
    image: tim/nginx-proxy
    container_name: nginx-proxy-server
    env_file:
      - ./webserver/config.env
    volumes:
      - nginx_conf:/etc/nginx/sites
      - letsencrypt_certs:/etc/letsencrypt
      - certbot_acme_challenge:/var/www/certbot
      - ./webserver/vhosts:/etc/nginx/vhosts
      - ./webserver/html:/var/www/html
    ports:
      - "80:80"
      - "443:443"
    restart: unless-stopped

RUN apk add --no-cache bash

COPY certbot.sh /opt/

RUN chmod +x /opt/certbot.sh

ENTRYPOINT ["/opt/certbot.sh"]