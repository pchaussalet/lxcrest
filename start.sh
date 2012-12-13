#!/usr/bin/env bash
PORT=$1
if [ "A$PORT" == "A" ]
then
  PORT=8080
fi
uwsgi -H venv --http-socket :$PORT -w server:app
