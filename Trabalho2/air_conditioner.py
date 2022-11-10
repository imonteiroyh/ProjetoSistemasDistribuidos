import grpc
from concurrent import futures
from proto.air_conditioner_pb2_grpc import add_AirConditionerServicer_to_server
from config import HOST, AIR_CONDITIONER_PORT
from components.temperature_sensor import TemperatureSensor
from components.air_conditioner_actuator import AirConditionerActuator

temperature_sensor = TemperatureSensor(HOST)
temperature_sensor.run()

server = grpc.server(futures.ThreadPoolExecutor(max_workers = 10))
air_conditioner_actuator = AirConditionerActuator(temperature_sensor.change_target, temperature_sensor.change_state)

add_AirConditionerServicer_to_server(air_conditioner_actuator, server)

server.add_insecure_port(HOST + ':' + AIR_CONDITIONER_PORT)
server.start()
server.wait_for_termination()