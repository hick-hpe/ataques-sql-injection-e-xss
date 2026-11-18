build:
	docker compose up -d --build

up:
	docker compose up -d

down:
	docker compose down

ps:
	docker compose ps

logs:
	docker compose logs -f

db:
	docker exec -it mysql_lab mysql -u app_user -p