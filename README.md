# Athenian Dashboard API

- As I'm using background tasks on the upload endpoint, I created an Operation model to record and process data load operations in the application.
- In the endpoint of the dash it is possible after creating a visualization to put the uid and visualize the generated graph.

## Documentation
    `http://localhost:5000/docs`

## Dash
    `http://localhost:5000/dash/`

## Running app
    `make run`

* After starting the application, it is necessary to run the database migrations.

    `make setup-db`

## Down app
    `make down`

## Logs app
    `make logs`

## Testing app
    `make test`
