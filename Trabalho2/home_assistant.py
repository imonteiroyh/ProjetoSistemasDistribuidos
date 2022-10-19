import grpc
import lamp_pb2 as lamp
import lamp_pb2_grpc


def main():
    with grpc.insecure_channel('localhost:5000') as channel:
        lamp_service = lamp_pb2_grpc.LampStub(channel)
        lamp_state = lamp_service.retrieve_state(lamp.EmptyRequest())
        print(f'Lamp state: {lamp_state}')


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit(0)
