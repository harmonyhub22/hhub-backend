docker-compose up -d

$env:FLASK_APP = "app"
$env:FLASK_ENV = "development"

flask db init
flask db migrate
flask db upgrade

flask run