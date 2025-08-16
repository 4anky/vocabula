build-web:  # Собирает образ веб-сервера без использования кеширования
	docker build -t vocabula --no-cache -f docker/Dockerfile .

run-web:  # Запускает контейнер веб-сервера
	docker run -p 8000:8000 -d vocabula

rm-web:
	docker stop $(docker ps -aq) && docker rm $(docker ps -aq)
