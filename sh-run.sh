#!/bin/bash

docker-compose up -d

export FLASK_APP=app
export FLASK_ENV=development

flask db init
flask db migrate
flask db upgrade

flask run