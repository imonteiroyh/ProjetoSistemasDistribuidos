import pika
import threading
from random import randint
from time import sleep
from config import TEMPERATURE_SENSOR_EXCHANGE

class TemperatureSensor:

    def __init__(self, RABBITMQ_HOST, target=20):
        self.exchange_name = TEMPERATURE_SENSOR_EXCHANGE
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(RABBITMQ_HOST))
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange=self.exchange_name, exchange_type='fanout')
        print('Temperature sensor connected to RabbitMQ')
        self.target = target
        self.temperature = target

    def generate_data(self):
        print('Generating data...')
        while True:
            if self.temperature > self.target:
                self.temperature -= 1
            elif self.temperature < self.target:
                self.temperature += 1

            self.channel.basic_publish(
                exchange=self.exchange_name,
                routing_key='',
                body=str(self.temperature)
            )
            sleep(5)
        
    def change_target(self, target):
        self.target = target

    def run(self):
        temperature_sensor_thread = threading.Thread(target=self.generate_data)
        temperature_sensor_thread.start()