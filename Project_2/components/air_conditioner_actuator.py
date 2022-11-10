from proto.air_conditioner_pb2 import AirConditionerResponse
from proto.air_conditioner_pb2_grpc import AirConditionerServicer

class AirConditionerActuator(AirConditionerServicer):
    def __init__(self, change_temperature_callback, change_sensor_state_callback) -> None:
        self.state = True
        self.temperature = 20
        self.callback = change_temperature_callback
        self.callback(self.temperature)
        self.change_sensor_state_callback = change_sensor_state_callback
        super().__init__()

    def get_temperature(self, request, context):
        return AirConditionerResponse(status=True, message = f'{self.temperature}')

    def change_temperature(self, request, context):
        self.temperature = int(request.temperature)
        self.callback(self.temperature)
        return AirConditionerResponse(status=True, message=f'Temperature setted to {self.temperature}')

    def change_state(self, request, context):
        self.state = request.state
        if self.state == True:
            self.callback(self.temperature)
        else:
            self.callback(25)

        message_complement = 'on' if self.state == True else 'off'
        return AirConditionerResponse(status=True, message=f'Air Conditioner is {message_complement}')

    def get_state(self, request, context):
        return AirConditionerResponse(status=True, message='on' if self.state == True else 'off')

    def change_sensor_state(self, request, context):
        self.change_sensor_state_callback(request.state)
        return AirConditionerResponse(status=True, message='Sensor is on' if request.state == True else 'Sensor is off')