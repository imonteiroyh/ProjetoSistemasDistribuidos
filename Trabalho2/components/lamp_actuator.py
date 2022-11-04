from proto.lamp_pb2 import LampResponse
from proto.lamp_pb2_grpc import LampServicer

class LampActuator(LampServicer):
    def __init__(self) -> None:
        self.state = True
        self.smart_lamp = True
        self.color = "white"
        super().__init__()

    def get_state(self, request, context):
        return LampResponse(status=True, message=f'{self.state}')

    def get_color(self, request, context):
        return LampResponse(status=True, message=f'{self.color}')

    def change_state(self, request, context):
        self.smart_lamp = False
        self.state = bool(request.state)
        return LampResponse(status=True, message=f'Lamp state setted to {self.state}')

    def change_color(self, request, context):
        self.color = request.color
        return LampResponse(status=True, message=f'Lamp color setted to {self.color}')

    def change_smart_lamp_state(self, request, context):
        self.smart_lamp = bool(request.state)
        return LampResponse(status=True, message=f'Smart Lamp state setted to {self.smart_lamp}')

    def change_state_from_motion(self, motion):
        if self.smart_lamp == True:
            if motion == 0:
                self.state = False
            else:
                self.state = True
        return LampResponse(status=True, message=f'Lamp state setted to {self.state} from motion')