import grpc
import threading
import pika
from config import HOST, AIR_CONDITIONER_PORT, TEMPERATURE_SENSOR_EXCHANGE, MOTION_SENSOR_EXCHANGE, LAMP_PORT
from proto.air_conditioner_pb2_grpc import AirConditionerStub
from proto.lamp_pb2_grpc import LampStub
from callbacks import temperature_sensor_callback, motion_sensor_callback

class Actuators:
    def __init__(self):
        air_conditioner_channel = grpc.insecure_channel(HOST + ':' + AIR_CONDITIONER_PORT)
        self.air_conditioner_actuator = AirConditionerStub(air_conditioner_channel)

        lamp_channel = grpc.insecure_channel(HOST + ':' + LAMP_PORT)
        self.lamp_actuator = LampStub(lamp_channel)

class Sensors:
    def __init__(self):
        air_conditioner_thread = ThreadedConsumer(TEMPERATURE_SENSOR_EXCHANGE, temperature_sensor_callback)
        air_conditioner_thread.start()

        lamp_thread = ThreadedConsumer(MOTION_SENSOR_EXCHANGE, motion_sensor_callback)
        lamp_thread.start()

class ThreadedConsumer(threading.Thread):
    def __init__(self, exchange, callback):
        threading.Thread.__init__(self, daemon=True)
        parameters = pika.ConnectionParameters(HOST)
        connection = pika.BlockingConnection(parameters)
        self.channel = connection.channel()
        self.channel.exchange_declare(exchange=exchange, exchange_type='fanout')
        self.queue = self.channel.queue_declare(queue='', exclusive=True)
        self.queue_name = self.queue.method.queue
        self.channel.queue_bind(exchange=exchange, queue=self.queue_name)
        self.exchange = exchange

        self.channel.basic_consume(
            queue=self.queue_name,
            on_message_callback=callback,
            auto_ack=True
        )

        threading.Thread(target=self.channel.basic_consume(self.queue_name, on_message_callback=callback))

    def run(self):
        print(f'Starting thread to consume from exchange {self.exchange}...')
        self.channel.start_consuming()