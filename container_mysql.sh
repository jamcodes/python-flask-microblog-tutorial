#!/bin/bash -e
docker run --name mysql -d --rm \
    -e MYSQL_RANDOM_ROOT_PASSWORD=yes \
    -e MYSQL_DATABASE=microblog \
    -e MYSQL_USER=microblog \
    -e MYSQL_PASSWORD=1234 \
    mysql/mysql-server:5.7
