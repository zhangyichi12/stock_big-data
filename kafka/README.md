# Kafka

## data-producer.py
Implement a kafka producer, fetch one stock information from Yahoo finance every 5 seconds(can be modified) 
and send it to Kafka.

### dependecies
googlefinance   https://pypi.python.org/pypi/googlefinance

kafka-python    https://github.com/dpkp/kafka-python

schedule        https://pypi.python.org/pypi/schedule

confluent-kafka https://github.com/confluentinc/confluent-kafka-python
```sh
pip install -r requirements.txt
```

### how to run

Kafka running on a docker-machine named 'bigdata' and ip address is 192.168.99.100

Three arguments:

mandatory:    `--stock_symbol` default is `.IXIC`(NASDAQ)

optional:     `--topic_name` default value is `stock-analyzer`

optional:     `--kafka_broker` default value is `127.0.0.1`

```sh
python simple-data-producer.py your_stock_name
```

or

```sh
python data-producer.py
```
