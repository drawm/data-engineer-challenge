
clean:
	./clean.sh
build:
	docker-compose build

# Run backing services while in dev
dev: clean
	docker-compose up dwh users cards -d
	docker-compose up etl

ps:
	docker-compose ps

stop:
	docker-compose stop

logs:
	docker-compose logs -f

rerun: build clean
	docker-compose up
