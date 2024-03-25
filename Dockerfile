# syntax=docker/dockerfile:1

FROM python:3.10.14

COPY . .

RUN pip3 install -r ./requirements.txt

RUN chmod +x ./docker-entrypoint.sh
ENTRYPOINT [ "./docker-entrypoint.sh" ]