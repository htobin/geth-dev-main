docker compose down
docker rm $(docker ps -a | grep geth)
docker rmi $(docker image ls)
docker volume rm $(docker volume ls| grep geth)
docker network rm $(docker network ls| grep geth)