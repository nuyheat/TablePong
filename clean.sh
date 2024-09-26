#!/bin/bash

# 모든 컨테이너 정지
docker stop $(docker ps -qa) 2>/dev/null

# 모든 컨테이너 삭제
docker rm $(docker ps -qa) 2>/dev/null

# 모든 이미지 삭제
docker rmi -f $(docker images -qa) 2>/dev/null

# 모든 볼륨 삭제
docker volume rm $(docker volume ls -q) 2>/dev/null

# 모든 네트워크 삭제
docker network rm $(docker network ls -q) 2>/dev/null
