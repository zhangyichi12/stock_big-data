# - read from kafka
# - do average
# - save data back

from kafka import KafkaProducer
from kafka.errors import KafkaError

import argparse  # OR use sys
import logging
import time
import json

from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils

# KAFKA_IP_ADDRESS = '159.203.87.185'
KAFKA_IP_ADDRESS = '192.168.99.100'
# KAFKA_IP_ADDRESS = '127.0.0.1'
KAFKA_PORT = '9092'


# - rdd: abstract of data
def process(timeobj, rdd):
    num_of_records = rdd.count()
    if num_of_records == 0:
        return

    # - for each rdd records, do something (take out the LastTradingPrice, json)
    # - for all the rdd records, sum up -> reduce
    price_sum = rdd\
        .map(lambda record: float(json.loads(record[1].decode('utf-8'))[0].get('LastTradePrice')))\
        .reduce(lambda a, b: a + b)
    print(price_sum)
    print(num_of_records)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--topic_name', help='the kafka topic to push to')
    parser.add_argument('--kafka_broker', help='location of kafka broker')

    # - parse arguments, default arguments
    args = parser.parse_args()
    topic_name = args.topic_name or 'stock-analyzer'
    kafka_broker = args.kafka_broker or (KAFKA_IP_ADDRESS + ':' + KAFKA_PORT)

    sc = SparkContext("local[2]", "StockAveragePrice")

    # - DEBUG, INFO, WARNING, ERROR
    sc.setLogLevel('ERROR')
    ssc = StreamingContext(sc, 5)

    # - setup a kafka stream
    # - KafkaUtils save us write a consumer all by ourselves
    directKafkaStream = KafkaUtils.createDirectStream(ssc, [topic_name], {'metadata.broker.list': kafka_broker})
    directKafkaStream.foreachRDD(process)

    ssc.start()
    ssc.awaitTermination()

