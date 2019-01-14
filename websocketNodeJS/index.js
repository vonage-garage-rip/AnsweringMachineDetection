const WebSocket = require('ws');

const ws = new WebSocket('ws://careangel-amd-detector.herokuapp.com/socket');

ws.on('open', function open() {
  // ws.send('something');
});

ws.on('message', function incoming(data) {
  console.log(data);
});