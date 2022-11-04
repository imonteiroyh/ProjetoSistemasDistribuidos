import grpc

from fastapi import FastAPI, Response, status
from pydantic import BaseModel
from typing import Union

from proto.air_conditioner_pb2 import GetAirConditionerTemperatureRequest, ChangeAirConditionerTemperatureRequest
from proto.lamp_pb2 import GetLampStateRequest, GetLampColorRequest, ChangeLampStateRequest, ChangeSmartLampStateRequest, ChangeLampColorRequest
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

    if request.command is None:
        response_config.status_code = status.HTTP_400_BAD_REQUEST
        response = {'message': "'command' is a required field"}
        return response

    #COMANDOS: VERIFICAR ESTADO, ATIVAR/DESATIVAR SMART_LAMP, LIGAR/DESLIGAR LÂMPADA
    if request.command == 'get_state':
        actuator_request = GetLampStateRequest()
        try:
            actuator_response = actuators.lamp_actuator.get_state(actuator_request)
            if actuator_response.status == True:
                if actuator_response.message == "True":
                    current_state = 'on'
                else:
                    current_state = 'off'
                response = {'turned ': current_state}
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

    if request.command == 'get_color':
        actuator_request = GetLampColorRequest()

        try:
            actuator_response = actuators.lamp_actuator.get_color(actuator_request)
            if actuator_response.status == True:
                response = {'color': str(actuator_response.message)}
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

    if request.command == 'change_state':
        if request.arguments is None:
            response_config.status_code = status.HTTP_400_BAD_REQUEST
            response = {'message': "'arguments' is a required field for this command"}
            return response

        if str(request.arguments) not in ["0", "1"]:
            response_config.status_code = status.HTTP_400_BAD_REQUEST
            response = {'message': "'argument' must be 0 for turn off or 1 to turn on"}
            return response

        actuator_request = ChangeLampStateRequest(state=int(request.arguments))
        try:
            actuator_response = actuators.lamp_actuator.change_state(actuator_request)
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

    if request.command == 'change_smart_lamp_state':
        if request.arguments is None:
            response_config.status_code = status.HTTP_400_BAD_REQUEST
            response = {'message': "'arguments' is a required field for this command"}
            return response

        if str(request.arguments) not in ["0", "1"]:
            response_config.status_code = status.HTTP_400_BAD_REQUEST
            response = {'message': "'argument' must be 0 for turn off or 1 to turn on"}
            return response

        actuator_request = ChangeSmartLampStateRequest(state=int(request.arguments))
        try:
            actuator_response = actuators.lamp_actuator.change_smart_lamp_state(actuator_request)
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

    if request.command == 'change_color':
        if request.arguments is None:
            response_config.status_code = status.HTTP_400_BAD_REQUEST
            response = {'message': "'arguments' is a required field for this command"}
            return response

        if str(request.arguments) not in ['white', 'red', 'green', 'blue', 'yellow', 'orange', 'cyan']:
            response_config.status_code = status.HTTP_400_BAD_REQUEST
            response = {'message': "'argument' must be one off 'white', 'red', 'green', 'blue', 'yellow', 'orange', 'cyan' "}
            return response

        actuator_request = ChangeLampColorRequest(color=str(request.arguments))
        try:
            actuator_response = actuators.lamp_actuator.change_color(actuator_request)
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