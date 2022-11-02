from proto.lamp_pb2 import LampResponse
from proto.lamp_pb2_grpc import LampServicer

class LampActuator(LampServicer):
    def __init__(self) -> None:
        self.state = True
        self.smart_lamp = True
        super().__init__()

    def get_state(self, request, context):
        return LampResponse(status=True, message=f'{self.state}')

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