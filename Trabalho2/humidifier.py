import grpc
from concurrent import futures
from proto.humidifier_pb2_grpc import add_HumidifierServicer_to_server
from config import HOST, HUMIDIFIER_PORT
from components.humidity_sensor import HumiditySensor
from components.humidifier_actuator import HumidifierActuator

humidity_sensor = HumiditySensor(HOST)
humidity_sensor.run()

server = grpc.server(futures.ThreadPoolExecutor(max_workers = 10))
humidifier_actuator = HumidifierActuator(humidity_sensor.change_increasing)

humidity_sensor.set_callback(humidifier_actuator.update_state)

add_HumidifierServicer_to_server(humidifier_actuator, server)

server.add_insecure_port(HOST + ':' + HUMIDIFIER_PORT)
server.start()
server.wait_for_termination()