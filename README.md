#Big-Data-Proj

###A high performance data processing distributed system using Apache Kafka, Apache Cassandra, and Apache Spark to analyze stock data (200k msg/s on one MacBook Pro).

### Using Docker on docker-machine on Mac OS.

1. Create docker-machine
```
docker-machine create --driver virtualbox --virtualbox-cpu-count 2 --virtualbox-memory 2048 bigdata
```
2. Map terminal to docker-machine
```
eval $(docker-machine env bigdata)
```

3. Zookeeper
```
docker run -d -p 2181:2181 -p 2888:2888 -p 3888:3888 --name zookeeper confluent/zookeeper
```

4. Kafka
```
docker run -d -p 9092:9092 -e KAFKA_ADVERTISED_HOST_NAME=`docker-machine ip bigdata` -e KAFKA_ADVERTISED_PORT=9092 --name kafka --link zookeeper:zookeeper confluent/kafka
```

5. Cassandra
```
docker run -d -p 7199:7199 -p 9042:9042 -p 9160:9160 -p 7001:7001 --name cassandra cassandra:3.7
```

6. Redis
```
docker run -d -p 6379:6379 --name redis redis:alpine
```

7. pyenv and virtualenv
Using `pyenv` as python version control and use `virtualenv` to isolate dependencies.
```
source python_env/bin/activate
```
to get into virtual environment.