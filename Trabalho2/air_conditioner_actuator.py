from ast import arg
import grpc
from concurrent import futures
import threading
from proto import air_conditioner_pb2
from proto import air_conditioner_pb2_grpc
from config import HOST, AIR_CONDITIONER_PORT
from random import randint
import pika
from time import sleep


class AirConditionerService(air_conditioner_pb2_grpc.AirConditionerServicer):

    def __init__(self) -> None:
        self.state = True
        super().__init__()

    def get_temperature(self, request, context):
        return air_conditioner_pb2.AirConditionerResponse(status = True, message = 'Temperature is 25')


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
        t = threading.Thread(target=self.generate_data)
        t.start()
       


def main():

    temperature_sensor = TemperatureSensor(HOST)
    temperature_sensor.run()

    # server = grpc.server(futures.ThreadPoolExecutor(max_workers = 10))
    # air_conditioner_pb2_grpc.add_AirConditionerServicer_to_server(AirConditionerService(), server)
    # server.add_insecure_port(HOST + ':' + AIR_CONDITIONER_PORT)
    # server.start()
    # print('Funcionando')
    # server.wait_for_termination()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit(0)