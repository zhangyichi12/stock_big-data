from kafka import KafkaProducer

import time

# SERVER_IP_ADDRESS = '159.203.87.185'
SERVER_IP_ADDRESS = '192.168.99.100'

producer = KafkaProducer(bootstrap_servers=SERVER_IP_ADDRESS)
producer.send(topic='stock-analyzer', value='HELLOWORLD', timestamp_ms=time.time())