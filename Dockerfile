FROM ubuntu:latest
LABEL authors="VKURTA"

ENTRYPOINT ["top", "-b"]

FROM postgres:latest

ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=postgres
ENV POSTGRES_DB=postgres

COPY init.sql /docker-entrypoint-initdb.d/

EXPOSE 5432
