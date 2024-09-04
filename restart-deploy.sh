docker stop genai-app
docker rm genai-app
docker rmi genai-image
docker-compose up build
docker-compose up -d