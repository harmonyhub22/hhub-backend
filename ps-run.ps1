docker-compose down
docker rmi hhub-db:latest
docker-compose up -d

$env:FLASK_APP = "app"
$env:FLASK_ENV = "development"

flask db migrate
flask db upgrade

flask run