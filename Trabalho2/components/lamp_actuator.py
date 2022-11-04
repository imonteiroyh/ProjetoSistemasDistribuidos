from proto.lamp_pb2 import LampResponse
from proto.lamp_pb2_grpc import LampServicer

class LampActuator(LampServicer):
    def __init__(self) -> None:
        self.state = True
        self.smart_lamp = True
        super().__init__()

    def get_state(self, request, context):
        return LampResponse(status=True, message=f'{self.state}')

    def set_smart_lamp_state(self, request, context):
        self.smart_lamp = bool(request.smart_lamp_state)
        return LampResponse(status=True, message=f'Smart Lamp State setted to {self.smart_lamp_state}')

    def set_lamp_state(self, request, context):
        self.smart_lamp = False
        self.state = bool(request.lamp_state)
        return LampResponse(status=True, message=f'Lamp State setted to {self.state}')

    # def get_motion(self, request, context):
    #     return LampResponse(status=True, message = f'{self.motion}')

    # def change_smart_lamp(self, request, context):
    #     self.smart_lamp = int(request.smart_lamp)
    #     self.callback(self.smart_lamp)
    #     return LampResponse(status=True, message=f'Smart Lamp setted to {self.smart_lamp}')

    def set_state_from_motion(self, motion):
        if self.smart_lamp == True:
            if motion == 0:
                self.state = False
            else:
                self.state = True
        return LampResponse(status=True, message=f'State setted to {self.state}')

    # def get_temperature(self, request, context):
    #     return AirConditionerResponse(status=True, message = f'{self.temperature}')

    # def change_temperature(self, request, context):
    #     self.temperature = int(request.temperature)
    #     self.callback(self.temperature)
    #     return AirConditionerResponse(status=True, message=f'Temperature setted to {self.temperature}')