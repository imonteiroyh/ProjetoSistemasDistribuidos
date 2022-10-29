from config import HOST
import pika
import threading

class ThreadedConsumer(threading.Thread):
    def __init__(self, exchange, callback):
        threading.Thread.__init__(self)
        parameters = pika.ConnectionParameters(HOST)
        connection = pika.BlockingConnection(parameters)
        self.channel = connection.channel()
        self.channel.exchange_declare(exchange=exchange, exchange_type='fanout')
        self.queue = self.channel.queue_declare(queue='', exclusive=True)
        self.queue_name = self.queue.method.queue
        self.channel.queue_bind(exchange=exchange, queue=self.queue_name)

        print('Waiting for data...')

        self.channel.basic_consume(
            queue=self.queue_name,
            on_message_callback=callback,
            auto_ack=True
        )

        threading.Thread(target=self.channel.basic_consume(self.queue_name, on_message_callback=callback))

    def run(self):
        print('Starting thread to consume from rabbit...')
        self.channel.start_consuming()