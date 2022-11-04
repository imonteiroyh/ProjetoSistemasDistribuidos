import pika
import threading
from random import randint
from time import sleep
from config import MOTION_SENSOR_EXCHANGE

class MotionSensor:

    def __init__(self, RABBITMQ_HOST, change_motion_callback):
        self.exchange_name = MOTION_SENSOR_EXCHANGE
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(RABBITMQ_HOST))
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange=self.exchange_name, exchange_type='fanout')
        print('Motion sensor connected to RabbitMQ')
        self.callback = change_motion_callback

    def generate_data(self):
        print('Generating data...')
        while True:
            self.motion = randint(0, 1)
            self.callback(self.motion)

            self.channel.basic_publish(
                exchange=self.exchange_name,
                routing_key='',
                body=str(self.motion)
            )
            sleep(5)

    def run(self):
        motion_sensor_thread = threading.Thread(target=self.generate_data)
        motion_sensor_thread.start()