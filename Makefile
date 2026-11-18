build:
	docker compose up -d --build

up:
	docker compose up -d

down:
	docker compose down

downv:
	docker compose down -v

ps:
	docker compose ps

logs:
	docker compose logs -f

db-root:
	docker exec -it mysql_lab mysql -u root -p

db:
	docker exec -it mysql_lab mysql -u app_user -p