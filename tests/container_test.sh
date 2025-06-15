# Test Docker build
docker build -t travel-assistant .

# Test Docker run
docker run -d --name test-app -p 8000:80 travel-assistant
curl http://localhost:8000/health