import grpc
from concurrent import futures
from proto import blind_curtain_pb2
from proto import blind_curtain_pb2_grpc

class BlindCurtainService(blind_curtain_pb2_grpc.BlindCurtainServicer):

    def __init__(self) -> None:
        self.state = True
        super().__init__()

    def get_state(self, request, context):
        return blind_curtain_pb2.BlindCurtainResponse(status = True, message = 'Open')

def main():
    port = '5000'
    server = grpc.server(futures.ThreadPoolExecutor(max_workers = 10))
    blind_curtain_pb2_grpc.add_BlindCurtainServicer_to_server(BlindCurtainService(), server)
    server.add_insecure_port('localhost:' + port)
    server.start()
    print('Funcionando')
    server.wait_for_termination()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit(0)