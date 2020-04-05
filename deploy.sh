#!/bin/bash

docker build -t adriankubica/fastapi -f Dockerfile .
docker push adriankubica/fastapi

docker build -t adriankubica/fastapi-nginx-proxy ./nginx-reverse-proxy
docker push adriankubica/fastapi-nginx-proxy

ssh root@165.22.69.128 'docker pull adriankubica/fastapi'
ssh root@165.22.69.128 'docker pull adriankubica/fastapi-nginx-proxy'
ssh root@165.22.69.128 'docker rm -f fastapi'
ssh root@165.22.69.128 'docker rm -f fastapi-nginx-proxy'
ssh root@165.22.69.128 'docker run -d -it --name fastapi -e MODULE_NAME="app" -e PORT="8000" -e MODE="PRODUCTION" -p 8000:8000 adriankubica/fastapi'
ssh root@165.22.69.128 'docker run -d -it --name fastapi-nginx-proxy -p 80:80 adriankubica/fastapi-nginx-proxy'
