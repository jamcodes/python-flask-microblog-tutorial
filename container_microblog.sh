#!/bin/bash -e
docker run --name microblog -d --rm \
    -p 8000:5000 \
    -e SECRET_KEY=test-secret-key \
    -e MAIL_SERVER=localhost \
    -e MAIL_PORT=8025 \
    -e MAIL_USE_TLS=true \
    --link mysql:dbserver \
    -e DATABASE_URL=mysql+pymysql://microblog:1234@dbserver/microblog \
    --link elasticsearch:elasticsearch \
    -e ELASTICSEARCH_URL=http://elasticsearch:9200 \
    microblog:latest
    # -e MAIL_USERNAME=<your-gmail-username> \
    # -e MAIL_PASSWORD=<your-gmail-password> \