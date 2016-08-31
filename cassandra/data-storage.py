from kafka import KafkaConsumer
from cassandra.cluster import Cluster

import argparse
import json
import logging
import atexit

#KAFKA_IP_ADDRESS = '159.203.87.185'
KAFKA_IP_ADDRESS = '192.168.99.100'
#KAFKA_IP_ADDRESS = '127.0.0.1'
KAFKA_PORT = '9092'

CASSANDRA_IP_ADDRESS = '192.168.99.100'


def save_data(cassandra_session, msg):
    print(msg)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--topic_name', help='the kafka topic to fetch from')
    parser.add_argument('--kafka_broker', help='location of kafka broker')
    parser.add_argument('--key_space', help='the keyspace of cassandra')
    parser.add_argument('--data_table', help='the data table to use')
    parser.add_argument('--cassandra_broker', help='the cassandra location')

    # - parse arguments, default arguments
    args = parser.parse_args()
    topic_name = args.topic_name or 'stock-analyzer'
    kafka_broker = args.kafka_broker or (KAFKA_IP_ADDRESS + ':' + KAFKA_PORT)
    key_space = args.key_space or 'stock'
    data_table = args.data_table or 'stock'
    cassandra_broker = args.cassandra_broker or CASSANDRA_IP_ADDRESS

    # - setup kafka consumer
    consumer = KafkaConsumer(topic_name, bootstrap_servers=kafka_broker)

    # - setup cassandra session
    cassandra_cluster = Cluster(contact_points=cassandra_broker.split(','))  # eg: host_ip_1, host_ip_2, ...
    session = cassandra_cluster.connect(key_space)

    for msg in consumer:
        save_data(session, msg)
