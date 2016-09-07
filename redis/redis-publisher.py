# - read form a kafka topic
# - publish data to redis PUB

from kafka import KafkaConsumer
import redis

import argparse
import time
import json
import logging
import schedule
import atexit


KAFKA_IP_ADDRESS = '159.203.87.185'
# KAFKA_IP_ADDRESS = '192.168.99.100'
KAFKA_PORT = '9092'
REDIS_IP_ADDRESS = '159.203.87.185'
# REDIS_IP_ADDRESS = '192.168.99.100'
REDIS_PORT = '6379'


# - config logging information
logging_format = '%(asctime)-15s %(message)s'
logging.basicConfig(format=logging_format)
logger = logging.getLogger('stream-process')
logger.setLevel(logging.INFO)  # TRACE, DEBUG, INFO, WARN, ERROR

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--topic_name', help='the kafka topic to push to')
    parser.add_argument('--kafka_broker', help='location of kafka broker')
    parser.add_argument('--redis_channel', help='the redis channel')  # - similar to kafka topic
    parser.add_argument('--redis_host', help='the ip/url of redis')
    parser.add_argument('--redis_port', help='the port of redis')

    # - parse arguments, default arguments
    args = parser.parse_args()
    topic_name = args.topic_name or 'spark-average-stock-price'
    kafka_broker = (args.kafka_broker or KAFKA_IP_ADDRESS) + ':' + KAFKA_PORT
    redis_channel = args.redis_channel or 'spark-average-stock-price'
    redis_host = args.redis_host or REDIS_IP_ADDRESS
    redis_port = args.redis_port or REDIS_PORT

    # - setup kafka consumer
    kafka_consumer = KafkaConsumer(topic_name, bootstrap_servers=kafka_broker)

    # - setup redis cline
    redis_client = redis.StrictRedis(host=redis_host, port=redis_port)

    for msg in kafka_consumer:
        logger.info('Received new data from kafka %s' % str(msg))
        redis_client.publish(redis_channel, msg.value)