const net = require('net');
const read = require('readline-sync');

const port = 8080;
const address = 'localhost';

const client = new net.Socket();

const firstValue = read.question('Type the first value: ');
const secondValue = read.question('Type the second value: ');
const operation = read.question('Type the operation: [+, -, *, /] ');
const type = read.question('Integer [i] or float [f] operation? ');

const message = buildMessage(firstValue, secondValue, operation, type);

client.connect(port, address, () => {
    console.log('Sending data...');
    client.write(message)
})

client.on('data', (stream) => {

    const result = stream.toString().split(' ');
    const status = result[0];
    result.shift();
    const message = result.join(' ');

    if (status == 'SUCCESS'){
        console.log(`Answer: ${message}`);
    }

    else if (status == 'ERROR') {
        console.log(`Error from server: ${message}`);
    }

    client.destroy();
    console.log('Connection closed');
});

function buildMessage(firstValue, secondValue, operation, type) {
    let formattedOperation;

    if (operation == '+') formattedOperation = 'SUM';
    else if (operation == '-') formattedOperation = 'SUB';
    else if (operation == '*') formattedOperation = 'MULT';
    else if (operation == '/') formattedOperation = 'DIV';
    else {
        console.log(`Error from client: invalid operation ${operation}`);
        process.exit();
    }

    let formattedType;

    if (type == 'i') formattedType = 'INTEGER';
    else if (type == 'f') formattedType = 'FLOAT';
    else {
        console.log(`Error from client: invalid type ${type}`);
        process.exit();
    }

    if (isNaN(firstValue)) {
        console.log(`Error from client: first value is not a number`);
        process.exit();
    }

    if (isNaN(secondValue)) {
        console.log(`Error from client: second value is not a number`);
        process.exit();
    }

    return `${firstValue} ${secondValue} ${formattedOperation} ${formattedType}`;
}