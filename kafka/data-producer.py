from kafka import KafkaProducer

import argparse
import time
import json
import logging
import schedule
import atexit

from googlefinance import getQuotes

# - SERVER_IP_ADDRESS = '159.203.87.185'
KAFKA_IP_ADDRESS = '192.168.99.100'
KAFKA_PORT = '9092'

# - config logging information
logging_format = '%(asctime)-15s %(message)s'
logging.basicConfig(format=logging_format)
logger = logging.getLogger('data-producer')
logger.setLevel(logging.DEBUG) # TRACE, DEBUG, INFO, WARN, ERROR

def fetch_price(producer, stock_symbol):
    price = json.dumps(getQuotes(stock_symbol))
    logger.debug('Get stock price %s', price)
    producer.send(topic=topic_name, value=price, timestamp_ms=time.time())
    logger.debug('Successfully sent data to Kafka')

def shutdown_hook(producer):
    logger.info('preparing to shutdown, waiting for producer to flush message')
    producer.flush(10) # send holding data first and stop fetching new data
    logger.info('producer flush finished')
    producer.close()
    logger.info('producer closed')

# - setup command line arguments
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('stock_symbol', help='the stock symbol')
    parser.add_argument('--topic_name', help='the kafka topic to push to')
    parser.add_argument('--kafka_broker', help='location of kafka broker')

    # - parse arguments, default arguments
    args = parser.parse_args()
    stock_symbol = args.stock_symbol
    topic_name = args.topic_name or 'stock-analyzer-2'
    kafka_broker = args.kafka_broker or (KAFKA_IP_ADDRESS + ':' + KAFKA_PORT)

    producer = KafkaProducer(bootstrap_servers=kafka_broker)

    # - schedule and run every second
    schedule.every().second.do(fetch_price, producer, stock_symbol)

    # - register shutdown hook
    atexit.register(shutdown_hook, producer)

    # - kick start schedule
    while True:
        schedule.run_pending()
        time.sleep(5)





