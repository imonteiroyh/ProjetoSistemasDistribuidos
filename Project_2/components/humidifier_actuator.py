from proto.humidifier_pb2 import HumidifierResponse
from proto.humidifier_pb2_grpc import HumidifierServicer

class HumidifierActuator(HumidifierServicer):
    def __init__(self, change_increase_calllback, change_sensor_state_callback) -> None:
        self.state = True
        self.smart_mode = True
        self.callback = change_increase_calllback
        self.callback(self.state)

        self.change_sensor_state_callback = change_sensor_state_callback

        self.upper = 55
        self.lower = 40

        super().__init__()

    def get_state(self, request, context):
        return HumidifierResponse(status=True, message = 'on' if self.state else 'off')

    def get_smart_humidifier_state(self, request, context):
        return HumidifierResponse(status=True, message = 'on' if self.smart_mode else 'off')

    def change_state(self, request, context):
        self.smart_mode = False
        self.callback(request.state)
        self.state = request.state
        return HumidifierResponse(
            status=True, 
            message='Humidifier state is setted to {}'.format('on' if request.state else 'off')
            )

    def change_smart_humidifier_state(self, request, context):
        self.smart_mode = request.state
        return HumidifierResponse(
            status=True,
            message='Smart Humidifier state is setted to {}'.format('on' if request.state else 'off')
        )

    def change_bounds(self, request, context):
        self.upper = request.upper_bound
        self.lower = request.lower_bound
        return HumidifierResponse(
            status=True,
            message=f'Upper bound setted to {self.upper} and lower bound setted to {self.lower}'
        )

    def update_state(self, humidity):
        if self.smart_mode == True:
            if humidity >= self.upper:
                self.state = False
                self.callback(False)
            elif humidity <= self.lower:
                self.state = True
                self.callback(True)
    
    def change_sensor_state(self, request, context):
        self.change_sensor_state_callback(request.state)
        return HumidifierResponse(status=True, message='Sensor is on' if request.state == True else 'Sensor is off')