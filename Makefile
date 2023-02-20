PORT ?= 5000
COMPOSE=docker-compose $(COMPOSE_OPTS)

run-local:	## run project
	uvicorn --host 0.0.0.0 --port $(PORT) main:app --lifespan=on --reload

run:
	$(COMPOSE) up -d

down:
	$(COMPOSE) down

# target: logs - Shows logs for api
logs:
	$(COMPOSE) logs -f api

# target: bash - Runs /bin/bash in App container for development
bash:
	$(COMPOSE) exec api /bin/bash

# target: alembic upgrade head
setup-db:
	$(COMPOSE) run --rm api alembic upgrade head

# target: alembic downgrade
downgrade:
	$(COMPOSE) run --rm api alembic downgrade $(version)

# target: alembic revision
alembic-revision:
	$(COMPOSE) run --rm api alembic revision --autogenerate -m $(msg)

# target: test
test:
	$(COMPOSE) run --rm api pytest
