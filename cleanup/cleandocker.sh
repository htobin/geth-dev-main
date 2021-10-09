docker compose down
docker rm $(docker ps -a -q)
docker rmi $(docker image ls)
docker volume rm $(docker volume ls)
docker network rm $(docker network ls)