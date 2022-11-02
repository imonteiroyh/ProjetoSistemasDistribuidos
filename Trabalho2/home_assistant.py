import grpc

from fastapi import FastAPI, Response, status
from pydantic import BaseModel
from typing import Union

from proto.air_conditioner_pb2 import GetAirConditionerTemperatureRequest, ChangeAirConditionerTemperatureRequest
from proto.lamp_pb2 import GetLampStateRequest
from utils import Actuators, Sensors


class ApplicationRequest(BaseModel):
    command: Union[str, None] = None
    arguments: Union[str, None] = None

sensors = Sensors()
actuators = Actuators()

app = FastAPI()

@app.post('/air_conditioner')
def air_conditioner_service(request: ApplicationRequest, response_config: Response):

    if request.command is None:
            response_config.status_code = status.HTTP_400_BAD_REQUEST
            response = {'message': "'command' is a required field"}
            return response

    if request.command == 'get_temperature':
        actuator_request = GetAirConditionerTemperatureRequest()

        try:
            actuator_response = actuators.air_conditioner_actuator.get_temperature(actuator_request)
            if actuator_response.status == True:
                response = {'temperature': int(actuator_response.message)}
            else:
                response_config.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
                response = {
                    'message': 'A error has occurred when the device was processing the request',
                    'device message': str(actuator_response.message)
                    }

        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.UNAVAILABLE:
                response_config.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
                response = {'message': 'Actuator unavailable'}

            else:
                print(e)
                response_config.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
                response = {'message': 'Unexpected error while communicating with the actuator'}

        except Exception as e:
            response_config.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            response = {'message': 'Unexpected error'}
        
        finally:
            return response

        

    if request.command == 'change_temperature':
        if request.arguments is None:
            response_config.status_code = status.HTTP_400_BAD_REQUEST
            response = {'message': "'arguments' is a required field for this command"}
            return response

        actuator_request = ChangeAirConditionerTemperatureRequest(temperature=str(request.arguments))
        try:
            actuator_response = actuators.air_conditioner_actuator.change_temperature(actuator_request)
            if actuator_response.status == True:
                response = {'message': actuator_response.message}
            else:
                response_config.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
                response = {
                    'message': 'A error has occurred when the device was processing the request',
                    'device message': str(actuator_response.message)
                    }
        
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.UNAVAILABLE:
                response_config.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
                response = {'message': 'Actuator unavailable'}

            else:
                print(e)
                response_config.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
                response = {'message': 'Unexpected error while communicating with the actuator'}

        except Exception as e:
            response_config.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            response = {'message': 'Unexpected error'}
        
        finally:
            return response


@app.post('/lamp')
def lamp(request: ApplicationRequest, response_config: Response):
    actuator_request = GetLampStateRequest()
    actuator_response = actuators.lamp_actuator.get_state(actuator_request)
    return {'state': actuator_response.message}