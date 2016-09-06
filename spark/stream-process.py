# - read from kafka
# - do average
# - save data back

import argparse  # OR use sys
import logging
import time
import json

# - spark
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils

# - send back to kafka
from kafka import KafkaProducer
from kafka.errors import KafkaError
import atexit

# KAFKA_IP_ADDRESS = '159.203.87.185'
KAFKA_IP_ADDRESS = '192.168.99.100'
# KAFKA_IP_ADDRESS = '127.0.0.1'
KAFKA_PORT = '9092'

# - config logging information
logging_format = '%(asctime)-15s %(message)s'
logging.basicConfig(format=logging_format)
logger = logging.getLogger('stream-process')
logger.setLevel(logging.DEBUG)  # TRACE, DEBUG, INFO, WARN, ERROR


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
    average_price = price_sum / num_of_records
    logger.info('Received records from Kafka, average price is %f' % average_price)
    current_time = time.time()
    data = json.dumps({'timestamp': current_time, 'average': average_price})

    # - handle exception
    try:
        kafka_producer.send(topic=new_topic_name, value=data)
    except KafkaError as error:
        logger.warn('Failed to send average stock price to kafka, caused by: %s', error.message)


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

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--topic_name', help='the kafka topic to push to')
    parser.add_argument('--kafka_broker', help='location of kafka broker')
    parser.add_argument('--new_topic_name', help='the kafka topic to push to')

    # - parse arguments, default arguments
    args = parser.parse_args()
    topic_name = args.topic_name or 'stock-analyzer'
    kafka_broker = args.kafka_broker or (KAFKA_IP_ADDRESS + ':' + KAFKA_PORT)
    new_topic_name = args.new_topic_name or 'spark-average-stock-price'

    sc = SparkContext("local[2]", "StockAveragePrice")

    # - DEBUG, INFO, WARNING, ERROR
    sc.setLogLevel('ERROR')
    ssc = StreamingContext(sc, 5)

    # - setup a kafka stream
    # - KafkaUtils save us write a consumer all by ourselves
    directKafkaStream = KafkaUtils.createDirectStream(ssc, [topic_name], {'metadata.broker.list': kafka_broker})
    directKafkaStream.foreachRDD(process)

    kafka_producer = KafkaProducer(bootstrap_servers=kafka_broker)

    # - register shutdown hook
    atexit.register(shutdown_hook, kafka_producer)

    ssc.start()
    ssc.awaitTermination()

