import pulsar
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

class Producer:
    def __init__(self, url: str, token: str, topic: str, op: Op):
        self._url = url
        self._token = token
        self._topic = topic
        self._op = op

    def generate_ids(self, ids_num=10000):
        ids = [random.random() for _ in range(ids_num)]
        return ids

    def send(self, vectors, ids=None):
        from pulsar import Client, AuthenticationToken

        client =  pulsar.Client(self._url, authentication=AuthenticationToken(self._token))
        producer = client.create_producer(self._topic, schema=AvroSchema(MilvusRecord))

        if ids is None:
            ids = self.generate_ids()
        assert(len(ids) >= len(vectors))

        for i in range(len(vectors)):
            producer.send(MilvusRecord(id=ids[i], op=self._op, vector=vectors[i]))
        
        client.close()


if __name__ == "__main__":
    import random

    url='pulsar://localhost:6650'
    token='eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1c2VyLTEifQ.8oAwbbd8dd3ZYhCWKAiShP4Kd0nHSwvQbTMX7Iat_o0'
    topic='persistent://public/default/topic0'
    op = Op.query
    _DIM = 16
    _VECTOR_NUM = 100

    vectors = [[random.random() for _ in range(_DIM)] for _ in range(_VECTOR_NUM)]
    ids = [i for i in range(_VECTOR_NUM)]

    producer = Producer(url=url, token=token, topic=topic, op=op)
    producer.send(vectors=vectors, ids=ids)
