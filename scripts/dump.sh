# /bin/bash

sudo docker-compose up -d --build neo4j

sudo chmod -R 777 ./db

ls ./db/data

wget -P ./db/data 'https://github.com/ICIJ/offshoreleaks-data-packages/raw/main/data/icij-offshoreleaks-44.dump'

docker exec -it neo4j ls -l /data

export _JAVA_OPTIONS="-Djava.io.tmpdir=/data"

docker exec -it neo4j bin/neo4j-admin load --from=/data/icij-offshoreleaks-44.dump --database=database --force --verbose

sudo chmod -R 777 ./db

echo "dbms.default_database=database" >> ./db/conf/neo4j.conf

sudo docker-compose up -d --build neo4j

sudo chmod -R 777 ./db

sudo cat ./db/conf/neo4j.conf
