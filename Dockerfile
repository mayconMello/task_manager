FROM ubuntu:latest
LABEL authors="maycon"

ENTRYPOINT ["top", "-b"]