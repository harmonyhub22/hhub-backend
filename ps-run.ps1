docker-compose down
docker-compose up -d

$env:FLASK_APP = "run.py"
$env:FLASK_ENV = "development"

flask run