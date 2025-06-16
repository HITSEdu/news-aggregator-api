build:
	docker-compose build
down:
	docker-compose down
up:
	make down
	docker-compose up -d