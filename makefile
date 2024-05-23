.PHONY: down build run start


DB_CONTAINER := blog_db
REDIS_CONTAINER := blog_redis
DB_TEST_VOLUME := $$(basename "$$(pwd)")_postgres_tests_data
REDIS_VOLUME := $$(basename "$$(pwd)")_redis_data

down:
	docker compose down

build:
	docker compose up -d --build

run: down
	docker compose up postgres redis -d
	@while true; do \
		sleep 1; \
		result_db=$$(docker inspect -f '{{json .State.Health.Status}}' $(DB_CONTAINER)); \
		result_redis=$$(docker inspect -f '{{json .State.Health.Status}}' $(REDIS_CONTAINER)); \
		if [ "$$result_db" = "\"healthy\"" ] && [ "$$result_redis" = "\"healthy\"" ]; then \
			echo "Services are healthy"; \
			break; \
		fi; \
	done
	alembic upgrade head
	make start

start:
	fastapi dev src

prod: down build

test:
	docker compose -f docker-compose-test.yml up -d postgres_tests
	pytest tests/
	docker stop postgres_tests
	docker rm postgres_tests
	if docker volume ls -q | grep -q $(DB_TEST_VOLUME); then \
		docker volume rm $(DB_TEST_VOLUME); \
		echo "successfully test_db";\
	fi
