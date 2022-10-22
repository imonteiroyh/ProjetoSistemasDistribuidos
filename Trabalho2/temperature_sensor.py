import pika
import threading
from random import randint
from time import sleep

class TemperatureSensor:

    def __init__(self, RABBITMQ_HOST):
        self.exchange_name = 'temperature_sensor'
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(RABBITMQ_HOST))
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange=self.exchange_name, exchange_type='fanout')
        print('Connected to RabbitMq')

    def generate_data(self):
        print('Generating data...')
        while True:
            temperature = randint(15, 30)
            self.channel.basic_publish(
                exchange=self.exchange_name,
                routing_key='',
                body=str(temperature)
            )
            sleep(5)

    def run(self):
        temperature_sensor_thread = threading.Thread(target=self.generate_data)
        temperature_sensor_thread.start()