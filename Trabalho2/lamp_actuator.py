import grpc
import lamp_pb2 as lamp
import lamp_pb2_grpc as lamp_service
from concurrent import futures


class LampService(lamp_service.LampServicer):

    def __init__(self) -> None:
        self.state = True
        super().__init__()

    def retrieve_state(self, request, context):
        return lamp.Response(status=True, message='Turned on')


def main():
    port = '5000'
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    lamp_service.add_LampServicer_to_server(LampService(), server)
    server.add_insecure_port('localhost:' + port)
    server.start()
    print('ouvindo')
    server.wait_for_termination()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit(0)
