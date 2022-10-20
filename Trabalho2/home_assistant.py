import grpc
from proto import lamp_pb2
from proto import lamp_pb2_grpc
from proto import air_conditioner_pb2
from proto import air_conditioner_pb2_grpc
from proto import blind_curtain_pb2
from proto import blind_curtain_pb2_grpc

def main():
    with grpc.insecure_channel('localhost:5000') as channel:
        lamp_service = lamp_pb2_grpc.LampStub(channel)
        lamp_state = lamp_service.get_state(lamp_pb2.GetLampStateRequest())
        print(f'Lamp state: {lamp_state}')
        # air_conditioner_service = air_conditioner_pb2_grpc.AirConditionerStub(channel)
        # air_conditioner_temperature = air_conditioner_service.get_temperature(air_conditioner_pb2.GetAirConditionerTemperatureRequest())
        # print(f'Air_conditioner temperature: {air_conditioner_temperature}')
        # blind_curtain_service = blind_curtain_pb2_grpc.BlindCurtainStub(channel)
        # blind_curtain_state = blind_curtain_service.get_state(blind_curtain_pb2.GetBlindCurtainStateRequest())
        # print(f'Blind Curtain state: {blind_curtain_state}')

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit(0)