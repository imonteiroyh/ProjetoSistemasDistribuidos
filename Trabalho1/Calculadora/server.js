const net = require('net');
const { TLSSocket } = require('tls');

const port = 8080;
const address = 'localhost';

const server = net.createServer();

function writeError(socket, message = 'An error occurred') {
    socket.write(`ERROR ${message}`);
    console.log(`Error from: ${socket.address().address}`);
    
    throw new Error(message);
}

server.on('connection', (socket) => {
    socket.on('data', (stream) => {
        
        const symbols = stream.toString().split(' ');

        if (symbols.length != 4) writeError(socket, 'invalid message format');

        const valueType = symbols[3];

        let firstValue, secondValue;

        if (valueType == 'FLOAT') {
            firstValue = parseFloat(symbols[0]);
            secondValue = parseFloat(symbols[1]);
        }
        else if (valueType == 'INTEGER') {
            firstValue = parseInt(symbols[0]);
            secondValue = parseInt(symbols[1]);
        }

        else writeError(socket, 'missing or invalid value type');

        const operation = symbols[2];
        let result;

        if (operation == 'SUM') result = firstValue + secondValue;
        else if (operation == 'SUB') result = firstValue - secondValue;
        else if (operation == 'MULT') result = firstValue * secondValue;
        else if (operation == 'DIV') result = firstValue / secondValue;
        else {
            writeError(socket, `invalid operation ${operation}`);
        }

        if (valueType == 'INTEGER') result = parseInt(result);

        socket.write(`SUCCESS ${result.toString()}`);
        socket.destroy();
    });

    socket.on('error', (error) => console.log(error));
});

server.listen(port, address, () => {
    console.log(`Listening on port ${port}...`);
});

process.on('uncaughtException', (error) => {
    console.log(`message: ${error.message}`);
});