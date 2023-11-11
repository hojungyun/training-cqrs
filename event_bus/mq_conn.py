import pika
import functools
import os
from retry import retry

# https://www.brandthill.com/blog/pika.html

class AmqpConnection:
    def __init__(self, hostname='localhost', port=5672, username='guest', password='guest'):
        self.hostname = hostname
        self.port = port
        self.username = username
        self.password = password
        self.connection = None
        self.channel = None

    def connect(self, connection_name='CQRS-Test-App'):
        print('Attempting to connect to', self.hostname)
        params = pika.ConnectionParameters(
            host=self.hostname,
            port=self.port,
            credentials=pika.PlainCredentials(self.username, self.password),
            client_properties={'connection_name': connection_name})
        self.connection = pika.BlockingConnection(parameters=params)
        self.channel = self.connection.channel()
        print('Connected Successfully to', self.hostname)

    def setup_queues(self):
        self.channel.exchange_declare('Product_Exchange', exchange_type='direct')
        self.channel.queue_declare('Product_Queue')
        self.channel.queue_bind('Product_Queue', exchange='Product_Exchange', routing_key='product')

    def do_async(self, callback, *args, **kwargs):
        if self.connection.is_open:
            self.connection.add_callback_threadsafe(functools.partial(callback, *args, **kwargs))

    def publish(self, payload: bytes):
        if self.connection.is_open and self.channel.is_open:
            self.channel.basic_publish(
                exchange='Product_Exchange',
                routing_key='product',
                body=payload
            )

    @retry(pika.exceptions.AMQPConnectionError, delay=1, backoff=2)
    def consume(self, on_message):
        if self.connection.is_closed or self.channel.is_closed:
            self.connect()
            self.setup_queues()
        try:
            self.channel.basic_consume(queue='Product_Queue', auto_ack=True, on_message_callback=on_message)
            self.channel.start_consuming()
        except KeyboardInterrupt:
            print('Keyboard interrupt received')
            self.channel.stop_consuming()
            self.connection.close()
            os._exit(1)
        except pika.exceptions.ChannelClosedByBroker:
            print('Channel Closed By Broker Exception')
