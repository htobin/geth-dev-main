docker compose down
docker rm -f $(docker ps -a | grep geth)
docker rmi -f $(docker image ls|grep geth)
docker volume rm -v $(docker volume ls| grep geth)
docker network rm -f $(docker network ls| grep geth)
