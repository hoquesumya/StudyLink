This microservice is responsible for creating the study groups per course
DB USER , DB_PASS AND DB_LOCALHOST SET UP:
create a .env file in the root directory of the project and read from that file
For Docker ---->
1. docker build: docker build --build-arg DB_HOST="$DB_HOST" --build-arg DB_PORT="$DB_PORT" --build-arg DB_USER="$DB_USER" --build-arg DB_PASSWORD="$DB_PASSWORD" -t sumya123/first_studygroup .
2. Docker run: docker run --name studygroup -p 8000:8000 --env DB_HOST=host.docker.internal --env DB_PORT=$DB_PORT --env DB_USER=$DB_USER --env DB_PASSWORD=$DB_PASSWORD sumya123/first_studygroup
Note: DB_HOST=host.docker.internal for localhost Database. Ovbiously it will change for the other db platform
3. docker ps for check running container
4. docker rm for remove a container
5. build for  multple platform:  docker buildx build --platform linux/amd64,linux/arm64 --build-arg DB_HOST="$DB_HOST" --build-arg DB_PORT="$DB_PORT" --build-arg DB_USER="$DB_USER" --build-arg DB_PASSWORD="$DB_PASSWORD" -t sumya123/first_studygroup --push .


