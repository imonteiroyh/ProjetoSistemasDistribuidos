def temperature_sensor_callback(ch, method, properties, body):
    print(f'Data received from temperature sensor: {int(body)}')

def motion_sensor_callback(ch, method, properties, body):
    print(f'Data received from motion sensor: {int(body)}')