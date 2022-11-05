import pika
import threading
from time import sleep
from config import HUMIDITY_SENSOR_EXCHANGE

class HumiditySensor:

    def __init__(self, RABBITMQ_HOST, initial_humidity=50, smart_mode_callback=None):
        self.exchange_name = HUMIDITY_SENSOR_EXCHANGE
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(RABBITMQ_HOST))

        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange=self.exchange_name, exchange_type='fanout')
        print('Humidity sensor connected to RabbitMQ')
        
        self.increasing = False
        self.humidity = initial_humidity

        self.callback = smart_mode_callback

    def generate_data(self):
        print('Generating data...')
        while True:
            if self.increasing == True:
                self.humidity = min(self.humidity + 1, 70)
            else:
                self.humidity = max(self.humidity - 1, 30)

            if self.callback is not None:
                self.callback(self.humidity)

            sleep(1)
            print(f'Humidity: {self.humidity}')
        
    def change_increasing(self, increasing):
        self.increasing = increasing

    def set_callback(self, callback):
        self.callback = callback

    def run(self):
        humidity_sensor_thread = threading.Thread(target=self.generate_data)
        humidity_sensor_thread.start()