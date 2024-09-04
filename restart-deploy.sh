docker stop genai-app
docker rm genai-app
docker rmi genai-image
docker-compose up build
docker-compose up -d

docker-compose exec -T app mkdir logs
docker-compose exec -T app chmod 755 logs
docker-compose exec -T app chmod 755 core/docs