FROM alpine:latest

RUN apk update;apk add python3 uwsgi
RUN pip3 install requests flask
