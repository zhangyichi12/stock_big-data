# Redis Proj

## redis-producer.py
Redis producer, get data from Kafka topic and publish it redis PUB.

### Dependencies
kafka-python    https://github.com/dpkp/kafka-python

redis           https://pypi.python.org/pypi/redis

```sh
pip install -r requirements.txt
```

### 运行代码
Kafka running on a docker-machine named 'bigdata' and ip address is 192.168.99.100
```sh
python redis-publisher.py 
```

