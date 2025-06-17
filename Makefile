build:
	docker-compose build
down:
	docker-compose down
up:
	make down
	docker-compose up

pg:
	docker-compose up postgres 

api:
	docker-compose up app