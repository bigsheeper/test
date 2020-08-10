import pulsar
import time
from pulsar import Client, AuthenticationToken
from pulsar import ConsumerType
from pulsar.schema import *
from enum import Enum

class Op(Enum):
    insert = 0
    delete = 1
    query = 2

class MilvusRecord(Record):
    id = Integer()
    op = Op
    vector = Array(Float())

def consumer_data(partition):
    client = pulsar.Client(service_url='pulsar://localhost:6650',
                           authentication=AuthenticationToken('eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1c2VyLTEifQ.8oAwbbd8dd3ZYhCWKAiShP4Kd0nHSwvQbTMX7Iat_o0'))
    consumer = client.subscribe(topic=partition,
                                subscription_name=partition,
                                schema=AvroSchema(MilvusRecord),
                                consumer_type=ConsumerType.Shared)

    while True:
        msg = consumer.receive()
        ex = msg.value()
        try:
            print("Received message id={} op={} vector={}".format(ex.id, ex.op, ex.vector))
            # Acknowledge successful processing of the message
            consumer.acknowledge(msg)
        except:
            # Message failed to be processed
            consumer.negative_acknowledge(msg)

    client.close()


consumer_data("persistent://public/default/topic0")