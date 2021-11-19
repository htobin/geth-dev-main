docker compose down
docker rm -f $(docker ps -a | grep geth)
docker rmi -f $(docker image ls|grep geth)
docker volume rm $(docker volume ls| grep geth)
docker network rm $(docker network ls| grep geth)
