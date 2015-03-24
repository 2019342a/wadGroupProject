#!/bin/bash

python server.py &
python manage.py runserver &

trap "kill -TERM -$$" SIGINT
wait
