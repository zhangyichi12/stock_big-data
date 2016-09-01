from kafka import KafkaConsumer
from cassandra.cluster import Cluster

import argparse
import json
import logging
import atexit

# KAFKA_IP_ADDRESS = '159.203.87.185'
KAFKA_IP_ADDRESS = '192.168.99.100'
# KAFKA_IP_ADDRESS = '127.0.0.1'
KAFKA_PORT = '9092'

CASSANDRA_IP_ADDRESS = '192.168.99.100'

# - config logging information
logging_format = '%(asctime)-15s %(message)s'
logging.basicConfig(format=logging_format)
logger = logging.getLogger('data-storage')
logger.setLevel(logging.DEBUG)  # TRACE, DEBUG, INFO, WARN, ERROR


def save_data(cassandra_session, value):
    # - msg is kafka ConsumerRecord Object
    parsed_data = json.loads(value)[0]
    stock_symbol = parsed_data.get('StockSymbol')
    trade_time = parsed_data.get('LastTradeDateTime')
    trade_price = float(parsed_data.get('LastTradePrice'))

    logger.info('received data from Kafka %s', parsed_data)

    # - use CQL statement to insert data
    statement = "INSERT INTO %s (stock_symbol, trade_time, trade_price) VALUES ('%s', '%s', %f)" % (data_table, stock_symbol, trade_time, trade_price)
    cassandra_session.execute(statement)
    logger.info('Saved data to cassandra, stock: %s, tradetime: %s, tradeprice: %f' % (stock_symbol, trade_time, trade_price))


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
        # logger.info(msg.value)
        save_data(session, msg.value)
