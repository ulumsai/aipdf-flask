docker stop genai-app2
docker rm genai-app2
docker rmi genai-image2
docker-compose -f docker-compose-local.yml up build --no-cache
docker-compose -f docker-compose-local.yml up -d
# docker-compose exec -T app mkdir logs
# docker-compose exec -T app chmod -R 777 logs
# docker-compose exec -T app chmod -R 777 core/docs