from config import HOST, LAMP_PORT
import grpc
from concurrent import futures
from motion_sensor import MotionSensor
from proto import lamp_pb2
from proto import lamp_pb2_grpc

class LampService(lamp_pb2_grpc.LampServicer):

    def __init__(self) -> None:
        self.state = True
        super().__init__()

    def get_state(self, request, context):
        return lamp_pb2.LampResponse(status=True, message='Turned on')

def main():

    motion_sensor = MotionSensor(HOST)
    motion_sensor.run()

    # server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    # lamp_pb2_grpc.add_LampServicer_to_server(LampService(), server)
    # server.add_insecure_port(HOST + ':' + LAMP_PORT)
    # server.start()
    # print('Funcionando')
    # server.wait_for_termination()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit(0)