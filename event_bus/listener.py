import orjson
import requests
from mq_conn import AmqpConnection


def on_message(channel, method, properties, body):
    product_data = orjson.loads(body)
    print(f"Creating product in NOSQL. {product_data=}")
    request_login = requests.post(
        "http://localhost:8001/products",
        json=product_data,
    )


def main():
    mq = AmqpConnection()
    mq.connect()
    mq.setup_queues()
    mq.consume(on_message)


if __name__ == '__main__':
    main()
