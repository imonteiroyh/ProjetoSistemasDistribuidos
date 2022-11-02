import grpc
from concurrent import futures
from proto.lamp_pb2_grpc import add_LampServicer_to_server
from config import HOST, LAMP_PORT
from components.motion_sensor import MotionSensor
from components.lamp_actuator import LampActuator

server = grpc.server(futures.ThreadPoolExecutor(max_workers = 10))
lamp_actuator = LampActuator()

motion_sensor = MotionSensor(HOST, lamp_actuator.set_state_from_motion)
motion_sensor.run()

add_LampServicer_to_server(lamp_actuator, server)

server.add_insecure_port(HOST + ':' + LAMP_PORT)
server.start()
server.wait_for_termination()