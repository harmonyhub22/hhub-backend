#!/bin/bash

docker-compose down
docker-compose up -d

export FLASK_APP=run.py
export FLASK_ENV=development

#flask db init
#flask db migrate
#flask db upgrade

flask run