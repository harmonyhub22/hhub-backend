#docker-compose down
#docker rmi hhub-db:latest
#docker-compose up

$env:FLASK_APP = "app"
$env:FLASK_ENV = "development"
flask run