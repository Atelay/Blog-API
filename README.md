<h1 align="center">Blog-API</h1>
<p align="center">
This project is a test assignment for a Python developer position. It is intended to demonstrate my skills and knowledge in FastAPI framework development.
The project does not aim to be perfect or complete, and it is not a production-ready product. It is a learning exercise created as part of the hiring process.
<p>

---

<h3 align="center">TECHNOLOGY</h3>
<p align="center">
  <a href="https://fastapi.tiangolo.com/" target="_blank">
    <img src="https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi" alt="FastAPI">
  </a>
  <a href="https://www.sqlalchemy.org/" target="_blank">
    <img src="https://img.shields.io/badge/sqlalchemy-fbfbfb?style=for-the-badge" alt="SQLAlchemy">
  </a>
  <a href="https://pydantic-docs.helpmanual.io/" target="_blank">
    <img src="https://img.shields.io/badge/Pydantic-14354C?style=for-the-badge&logo=Pydantic" alt="Pydantic-v2">
  </a>
</p>

<h2 align="center">INSTALLATION</h2>

To run the project, you will need [Docker-compose](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-compose-on-ubuntu-22-04) installed. Follow these steps to install and run the project:

1. Create a new folder for your project.

2. Open the project in an IDE

3. Initialize Git

    ```
    git init
    ```
4. Add the remote repository
    ```
    git remote add origin git@github.com:Atelay/Blog-API.git
    ```
5. Sync with the remote repository

    ```
    git pull origin main
    ```

6. Create a `.env` file and define all environment variables from the `.env.example` file:
    <details class="custom-details">
    <summary><b>DB settings</b></summary>
    <p class="custom-details-description"><i>Variables for database configuration.</i></p>

    <b class="variable-name">POSTGRES_PORT</b>=<span class="variable-value">5432</span><br>
    <b class="variable-name">POSTGRES_DB</b>=<span class="variable-value">blog_db</span><br>
    <b class="variable-name">POSTGRES_USER</b>=<span class="variable-value">postgres</span><br>
    <b class="variable-name">POSTGRES_PASSWORD</b>=<span class="variable-value">postgres</span><br>
    <b class="variable-name">REDIS_PASS</b>=<span class="variable-value">redis</span><br>
    <b class="variable-name">REDIS_URL</b>=<span class="variable-value">redis://default:redis@localhost:6379</span><br>
    <b class="variable-name">DB_URL</b>=<span class="variable-value">postgresql+asyncpg://postgres:postgres@localhost:5432/blog_db</span><br>

    </details>

<h2 align="center">USAGE</h2>

1. Create a virtual environment:
    ```
    python -m venv venv
    ```
2. Install dependencies:
    ```
    pip install -r requirements.txt
    ```
3. Run the project using the Makefile command:
    ```
    make run
    ```
    This command will create a container with the database, redis, initiate migrations, and start the server on port `8000`.<br>
    Subsequent launches of the application are carried out with the command:
    ```
    make start
    ```
<h2 align="center">MAKEFILE COMMANDS</h2>

*These commands streamline various development and deployment tasks, including container management, database operations, backups, and frontend management.*


- `down:` Stop and remove all Docker containers.
- `build`: Builds Docker images for the project.
- `run`: Starts Postgres containers for Postgres and Redis, waits for it to become healthy, upgrades the database, and then launches the application.
- `start`: Initiates the web application using Uvicorn.
- `test`: Runs the test suite

<h2 align="center">DOCUMENTATION</h2>

Interactive documentation is available at `/docs` and `/redoc` for two different interfaces: [Swagger](https://swagger.io/) and [ReDoc](https://redoc.ly/). They allow you to view and test all the API endpoints, as well as get information about the parameters, data types, and response codes. You can learn more about Swagger and ReDoc on their official websites.

<p align="center">
  <a href="https://swagger.io/" target="_blank">
    <img src="https://img.shields.io/badge/Swagger-85EA2D?style=for-the-badge&logo=swagger&logoColor=black" alt="Swagger">
  </a>
  <a href="https://redoc.ly/" target="_blank">
    <img src="https://img.shields.io/badge/Redoc-8A2BE2?style=for-the-badge&logo=redoc&logoColor=white" alt="Swagger">
  </a>
</p>