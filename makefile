run: stop up

up:
	docker compose -f docker-compose.yml up --build
	
stop:
	docker compose -f docker-compose.yml stop

down:
	docker compose -f docker-compose.yml down