const net = require('net');
const readline = require('readline');

const port = 8080;
const address = 'localhost';

const client = new net.Socket();

const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
});

rl.question('Digite o primeiro valor: ', (firstValue) => {
    rl.question('Digite o segundo valor: ', (secondValue) => {
        rl.question('Digite a operação: ', (operation) => {
            
            client.connect(port, address, () => {
                console.log('Sending data...');
                client.write(`${firstValue} ${operation} ${secondValue}`);
            });

            client.on('data', (stream) => {
                console.log(`Answer: ${stream}`);
            });

            client.on('close', () => console.log('Connection closed'));
            rl.close();
        });
    });
});





