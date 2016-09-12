# Spark Proj

## stream-process.py

### Dependencies
pyspark         http://spark.apache.org/docs/latest/api/python/

kafka-python    https://github.com/dpkp/kafka-python

```sh
pip install -r requirements.txt
```

### Run
Kafka running on a docker-machine named 'bigdata' and ip address is 192.168.99.100

```sh
spark-submit --jars spark-streaming-kafka-0-8-assembly_2.11-2.0.0.jar stream-processing.py
```