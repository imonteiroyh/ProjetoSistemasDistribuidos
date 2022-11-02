import pika
import threading
from random import randint
from time import sleep
from config import MOTION_SENSOR_EXCHANGE

class MotionSensor:

    def __init__(self, RABBITMQ_HOST):
        self.exchange_name = MOTION_SENSOR_EXCHANGE
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(RABBITMQ_HOST))
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange=self.exchange_name, exchange_type='fanout')
        print("Connected to RabbitMQ")

    def generate_data(self):
        print('Detecting movement...')
        while True:
            movement = randint(0, 1)
            self.channel.basic_publish(
                exchange=self.exchange_name,
                routing_key='',
                body=str(movement)
            )
            sleep(15)

    def run(self):
        motion_sensor_thread = threading.Thread(target=self.generate_data)
        motion_sensor_thread.start()