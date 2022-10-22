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
from temperature_sensor import TemperatureSensor


class AirConditionerService(air_conditioner_pb2_grpc.AirConditionerServicer):

    def __init__(self) -> None:
        self.state = True
        super().__init__()

    def get_temperature(self, request, context):
        return air_conditioner_pb2.AirConditionerResponse(status = True, message = 'Temperature is 25')

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