# Harmony Hub Backend

Built with Flask

<hr></hr>

## Description 

This is the frontend of the Harmony Hub application created by Team Musico for Senior CSCE 482 Capstone Spring 2022. The code contains REST api endpoints, socket-io endpoints, a PostgreSQL database implementation and connection, and AWS S3 bucket file storage logic.

## View Deployed Server

Visit the <a href="https://harmony-hub-backend.herokuapp.com/" target="_blank">Heroku Server</a>

## Spin-up Server locally

Set-up Instructions

1. Ensure Docker is installed on your system

2. Download the Docker PostgreSQL image

    Recommended image v13 (latest version Heroku Postgres supports):
    ```
    docker pull postgres:13.6-alpine
    ```

3. Get the Environment Variables file <code>.env</code> from a team member.

4. Create a virtual environment if you have not already

    ```
    python3 -m venv venv
    ```
   
5. Activate (enter) the virtual environment

    Windows
    ```
    . ./venv/Scripts/activate
    ```

    Mac
    ```
    source venv/bin/activate
    ```

6. Download the required packages

    ```
    pip install -r requirements.txt
    ```

7. Start the server and database

    Mac
    ```
    docker-compose down
    docker-compose up -d
    export FLASK_APP="run.py"
    export FLASK_ENV="development"
    flask run
    ```

    Windows
    ```
    docker-compose down
    docker-compose up -d
    $env:FLASK_APP="run.py"
    $env:FLASK_ENV="development"
    flask run
    ```
   
8. Visit in the browser

    Go to <a href="http://localhost:5000" target="_blank">Localhost Port 5000</a>


## Notes for Developers

I. To leave the python virtual environment, simply enter

```
deactivate
```

II. After adding a new pip library (eg. pip install ...), be sure to run

```
pip freeze > requirements.txt
```

III. To deploy to Production Server, add a Heroku remote as follows

```
heroku git:remote -a harmony-hub-backend # adds a heroku remote called heroku
git add .
git commit -m "deploying to production"
git push heroku master
```

IV. Enter the Local Postgres Datbase with the following command
(Docker Container: hhub-db)

```
psql -h localhost -p 5432 -U hhubuser -W
```
Password: literally anything

V. Trouble connecting to the local database?

Stop the Postgres Service on your local computer.

VI. For API endpoint reference, check out our

<a href="https://www.postman.com/orange-capsule-30931/workspace/hhub-backend" target="_blank">Postman Workspace</a>
