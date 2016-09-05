import express from 'express';
const app = express();

import redis from 'redis';

const redis_host = process.env.REDIS_HOST || '192.168.99.100';
const redis_port = process.env.REDIS_PORT || '6379';
const subscribe_channel = process.env.SUBSCRIBE_CHANNEL || 'spark-average-stock-price';

// create redis cline
var redisClient = redis.createClient(redis_port, redis_host);
console.log(`Subscribe to redis channel ${subscribe_channel}`);
redisClient.subscribe(subscribe_channel);

redisClient.on('message', (channel, message) => {
    console.log(`message received ${message}`);
});

//Start server
const serverPort = process.env.SERVER_PORT || 3001
app.listen(serverPort, () => {
    console.log(`Listening port ${serverPort}`);
});