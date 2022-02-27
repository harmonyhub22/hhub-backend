# Harmony Hub Backend

Built with Flask

<hr></hr>

**View Deployed Server**

Visit the <a href="https://harmony-hub-backend.herokuapp.com/" target="_blank">Heroku Server</a>

<hr></hr>

**Spin-up Server locally**

Set-up Instructions

1. Ensure Docker is installed on your system

2. Download the Docker PostgreSQL image

    Recommended image v13 (latest version Heroku Postgres supports):
    ```
    docker pull postgres:13.6-alpine
    ```

3. Get the Environment Variables file <code>.env</code> from a team member.

4. Enter the virtual environment

    ```
    python3 -m venv venv
    ```

    Windows
    ```
    . ./venv/Scripts/activate
    ```

    Mac
    ```
    source venv/bin/activate
    ```

5. Download the required packages

    ```
    pip install -r requirements.txt
    ```

6. Start the server and database

    Mac
    ```
    ./sh-run.sh
    ```

    Windows
    ```
    .\ps-run.ps1
    ```


To leave the virtual environment, simply enter <code>deactivate</code>

# Notes for Developers

I. After adding a new pip library, be sure to run

```
pip freeze > requirements.txt
```

II. To deploy to Production Server, add a Heroku remote as follows

```
git remote add heroku git@github.com:harmonyhub22/hhub-backend.git
```

III. Enter the Local Postgres Datbase with the following command
(Docker Container: hhub-db)

```
psql -h localhost -p 5432 -U hhubuser -W
```
Password: literally anything

IV. Trouble connecting to the local database?

Stop the Postgres Service on your local computer.

V. Look at the <a href="https://www.postman.com/orange-capsule-30931/workspace/hhub-backend" target="_blank">Postman Workspace</a> for api endpoint reference.
