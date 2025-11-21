FROM ubuntu:latest
LABEL authors="elise"

ENTRYPOINT ["top", "-b"]