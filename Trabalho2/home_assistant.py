from config import HOST, LAMP_PORT, AIR_CONDITIONER_PORT, BLIND_CURTAIN_PORT
import grpc
from proto import lamp_pb2
from proto import lamp_pb2_grpc
from proto import air_conditioner_pb2
from proto import air_conditioner_pb2_grpc
from proto import blind_curtain_pb2
from proto import blind_curtain_pb2_grpc
import pika
import threading

def temperature_sensor_callback(ch, method, properties, body):
    print(f'Data received from temperature sensor: {int(body)}')

def motion_sensor_callback(ch, method, properties, body):
    print(f'Data received from motion sensor: {int(body)}')

def main():

    connection = pika.BlockingConnection(pika.ConnectionParameters(HOST))
    channel = connection.channel()
    print('Connected to RabbitMQ')

    # temperature_sensor_thread = threading.Thread(target=subscribe, args=(channel, 'temperature_sensor', temperature_sensor_callback))
    # temperature_sensor_thread.start()

    motion_sensor_thread = threading.Thread(target=subscribe, args=(channel, 'motion_sensor', motion_sensor_callback))
    motion_sensor_thread.start()

    # with grpc.insecure_channel(HOST + ':' + LAMP_PORT) as LampChannel:
    #     lamp_service = lamp_pb2_grpc.LampStub(LampChannel)
    #     lamp_state = lamp_service.get_state(lamp_pb2.GetLampStateRequest())
    #     print(f'Lamp state: {lamp_state}')

    # with grpc.insecure_channel(HOST + ':' + AIR_CONDITIONER_PORT) as AirConditionerChannel:
    #     air_conditioner_service = air_conditioner_pb2_grpc.AirConditionerStub(AirConditionerChannel)
    #     air_conditioner_temperature = air_conditioner_service.get_temperature(air_conditioner_pb2.GetAirConditionerTemperatureRequest())
    #     print(f'Air_conditioner temperature: {air_conditioner_temperature}')

    # with grpc.insecure_channel(HOST + ':' + BLIND_CURTAIN_PORT) as BlindCurtainChannel:
    #     blind_curtain_service = blind_curtain_pb2_grpc.BlindCurtainStub(BlindCurtainChannel)
    #     blind_curtain_state = blind_curtain_service.get_state(blind_curtain_pb2.GetBlindCurtainStateRequest())
    #     print(f'Blind Curtain state: {blind_curtain_state}')

def subscribe(channel, exchange, callback):
    channel.exchange_declare(exchange=exchange, exchange_type='fanout')
    air_conditioner_queue = channel.queue_declare(queue='', exclusive=True)
    air_conditioner_queue_name = air_conditioner_queue.method.queue
    channel.queue_bind(exchange=exchange, queue=air_conditioner_queue_name)

    print('Waiting for data...')

    channel.basic_consume(
        queue=air_conditioner_queue_name,
        on_message_callback=callback,
        auto_ack=True
    )

    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit(0)