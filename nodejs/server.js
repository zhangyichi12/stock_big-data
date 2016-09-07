import express from 'express';
import http from 'http';
import socketio from 'socket.io';
import cors from 'cors';

const app = express();
const server = http.Server(app);
const io = socketio(server);

app.use(cors());
app.use((req, res, next) => {
    console.log(req.headers.host);
    // res.setHeader('Access-Control-Allow-Origin', "http://"+req.headers.host+':8080');
    res.setHeader('Access-Control-Allow-Origin', "http://"+'localhost'+':8080');
    res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS, PUT, PATCH, DELETE');
    res.setHeader('Access-Control-Allow-Headers', 'X-Requested-With,content-type');
    res.setHeader('Access-Control-Allow-Credentials', true);
    next();
});

import redis from 'redis';
const redis_host = process.env.REDIS_HOST || '159.203.87.185';
const redis_port = process.env.REDIS_PORT || '6379';
const subscribe_channel = process.env.SUBSCRIBE_CHANNEL || 'spark-average-stock-price';


io.on('connection', function(socket){
    console.log('socketio connected');
});

// create redis cline
var redisClient = redis.createClient(redis_port, redis_host);
console.log(`Subscribe to redis channel ${subscribe_channel}`);
redisClient.subscribe(subscribe_channel);

redisClient.on('message', (channel, message) => {
    console.log(`message received ${message}`);
    io.emit('stock-data', message);
});


//catch and handle error
app.use((err, req, res, next) => {                  //if err no exist, this wouldn't be excuted
    res.status(err.status || 500).send(err.message);
    next(err);
});

//Start server
const serverPort = process.env.SERVER_PORT || 3001
server.listen(serverPort, () => {
    console.log(`Listening port ${serverPort}`);
});

