

# Cassandra Proj

## data-storage.py
Get data from Kafka and save to Cassandra

### Dependencies
cassandra-driver    https://github.com/datastax/python-driver

cql

```sh
pip install -r requirements.txt
```

### Run
Cassandra running on a docker-machine named 'bigdata' and ip address is 192.168.99.100

### Create table in Cassandra
use cqlsh
```
wget http://apache.mirrors.ionfish.org/cassandra/3.7/apache-cassandra-3.7-bin.tar.gz
进入bin folder
export CQLSH_NO_BUNDLED=true
./cqlsh `docker-machine ip bigdata` 9042
```

create a keyspace and a table
```
CREATE KEYSPACE "stock" WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1} AND durable_writes = 'true';
USE stock;
CREATE TABLE stock (stock_symbol text, trade_time timestamp, trade_price float, PRIMARY KEY (stock_symbol,trade_time));
```

```sh
python data-storage.py
```
