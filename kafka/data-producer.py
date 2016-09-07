from kafka import KafkaProducer

import argparse
import time
import json
import logging
import schedule
import atexit

from googlefinance import getQuotes

# KAFKA_IP_ADDRESS = '159.203.87.185'
KAFKA_IP_ADDRESS = '192.168.99.100'
# KAFKA_IP_ADDRESS = '127.0.0.1'
KAFKA_PORT = '9092'

# - config logging information
logging_format = '%(asctime)-15s %(message)s'
logging.basicConfig(format=logging_format)
logger = logging.getLogger('data-producer')
logger.setLevel(logging.DEBUG)  # TRACE, DEBUG, INFO, WARN, ERROR


def fetch_price(producer, stock_symbol):
    """
    helper function to retrieve stock data and send it to kafka
    :param producer: instance of a kafka producer
    :param stock_symbol: symbol of the stock
    :return: None
    """
    price = json.dumps(getQuotes(stock_symbol))
    logger.debug('Get stock price %s', price)

    try:
        producer.send(topic=topic_name, value=price, timestamp_ms=time.time())
    except Exception:
        logger.warn('Failed to send message to kafka')

    logger.debug('Successfully sent data to Kafka')


def shutdown_hook(producer):
    """
    This a shutdown hook to be called before the shutdown
    :param producer: instance of a kafka producer
    :return: None
    """
    logger.info('preparing to shutdown, waiting for producer to flush message')
    producer.flush(10)  # send holding data first and stop fetching new data
    logger.info('producer flush finished')
    try:
        producer.close()
    except Exception:
        logger.warn('producer failed to close')
    logger.info('producer closed')

# - setup command line arguments
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--stock_symbol', help='the stock symbol')
    parser.add_argument('--topic_name', help='the kafka topic to push to')
    parser.add_argument('--kafka_broker', help='location of kafka broker')

    # - parse arguments, default arguments
    args = parser.parse_args()
    stock_symbol = args.stock_symbol or '.IXIC'
    topic_name = args.topic_name or 'stock-analyzer'
    kafka_broker = args.kafka_broker or (KAFKA_IP_ADDRESS + ':' + KAFKA_PORT)

    # - setup kafka producer
    producer = KafkaProducer(bootstrap_servers=kafka_broker)

    # - schedule and run every second
    schedule.every().second.do(fetch_price, producer, stock_symbol)

    # - register shutdown hook
    atexit.register(shutdown_hook, producer)

    # - kick start schedule
    while True:
        schedule.run_pending()
        time.sleep(1)
