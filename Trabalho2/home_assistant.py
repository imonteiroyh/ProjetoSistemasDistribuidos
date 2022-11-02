import grpc

from fastapi import FastAPI, Response, status
from pydantic import BaseModel
from typing import Union

from proto.air_conditioner_pb2 import GetAirConditionerTemperatureRequest, ChangeAirConditionerTemperatureRequest
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
            response = {'Message': "'command' is a required field"}
            return response

    if request.command == 'get_temperature':
        actuator_request = GetAirConditionerTemperatureRequest()

        try:
            actuator_response = actuators.air_conditioner_actuator.get_temperature(actuator_request)
            if actuator_response.status == True:
                response = {'Temperature': int(actuator_response.message)}
            else:
                response_config.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
                response = {
                    'Message': 'A error has occurred when the device was processing the request',
                    'Device Message': str(actuator_response.message)
                    }

        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.UNAVAILABLE:
                response_config.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
                response = {'Message': 'Actuator unavailable'}

            else:
                print(e)
                response_config.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
                response = {'Message': 'Unexpected error while communicating with the actuator'}

        except Exception as e:
            response_config.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            response = {'Message': 'Unexpected error'}
        
        finally:
            return response

        

    if request.command == 'change_temperature':
        if request.arguments is None:
            response_config.status_code = status.HTTP_400_BAD_REQUEST
            response = {'Message': "'arguments' is a required field for this command"}
            return response

        actuator_request = ChangeAirConditionerTemperatureRequest(temperature=str(request.arguments))
        try:
            actuator_response = actuators.air_conditioner_actuator.change_temperature(actuator_request)
            if actuator_response.status == True:
                response = {'Message': actuator_response.message}
            else:
                response_config.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
                response = {
                    'Message': 'A error has occurred when the device was processing the request',
                    'Device Message': str(actuator_response.message)
                    }
        
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.UNAVAILABLE:
                response_config.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
                response = {'Message': 'Actuator unavailable'}

            else:
                print(e)
                response_config.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
                response = {'Message': 'Unexpected error while communicating with the actuator'}

        except Exception as e:
            response_config.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            response = {'Message': 'Unexpected error'}
        
        finally:
            return response