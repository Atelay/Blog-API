.PHONY: down build run start


DB_CONTAINER := blog_db

down:
  docker compose down

build:
  docker compose up -d --build
  
run: down
  docker compose up postgres -d
  @while true; do \
    sleep 1; \
    result_db=$$(docker inspect -f '{{json .State.Health.Status}}' $(DB_CONTAINER)); \
    if [ "$$result_db" = "\"healthy\"" ]; then \
      echo "Service is healthy"; \
      break; \
    fi; \
  done
  alembic upgrade head
  make start

start:
  fastapi dev src
