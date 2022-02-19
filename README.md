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

3. Get the Environment Variables file <code>.env.local</code> from a team member.

4. Enter the virtual environment

    ```
    python3 -m venv venv
    . ./venv/Scripts/activate
    ```

5. Download the required packages

    ```
    pip install -r requirements.txt
    ```

5. Run the executable scripts

    Mac
    ```
    ./sh-run.sh
    ```

    Windows
    ```
    .\ps-run.ps1
    ```


To leave the virtual environment, simply enter <code>deactivate</code>
