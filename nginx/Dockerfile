FROM debian:7

RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y nginx openssl

ADD nginx.conf /etc/nginx/nginx.conf
RUN rm /etc/nginx/sites-enabled/*
ADD dinheiro.conf /etc/nginx/sites-enabled/dinheiro.conf

RUN mkdir /etc/nginx/conf.d/dinheiro
ADD start.sh /start

VOLUME /certs
EXPOSE 80
EXPOSE 443
ENTRYPOINT ["/bin/sh", "/start"]
