const net = require('net');

const port = 8080;
const address = 'localhost';

const server = net.createServer();

server.on('connection', (socket) => {
    socket.on('data', (stream) => {
        
        const symbols = stream.toString().split(' ');
        const firstValue = parseInt(symbols[0]);
        const secondValue = parseInt(symbols[2]);
        const operation = symbols[1];

        let result;

        if (operation == '+') result = firstValue + secondValue;
        else if (operation == '-') result = firstValue - secondValue;
        else if (operation == '*') resutl = firstValue * secondValue;
        else if (operation == '/') result = firstValue / secondValue;

        socket.write(result.toString());
        socket.destroy();
    });
});

server.listen(port, address, () => {
    console.log(`Listening on port ${port}...`);
});