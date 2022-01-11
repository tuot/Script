from __future__ import absolute_import, print_function, unicode_literals
from kombu import Exchange, Queue, Connection, Consumer, Producer

from kombu import Connection, Exchange, Producer, Queue


rabbitmq_url = "amqp://root:root@localhost:5672/"


task_queue = Queue('tasks',
                   exchange=Exchange(
                       'asd', type='direct'), routing_key='tasks')
# 生产者
with Connection(rabbitmq_url) as conn:
    with conn.channel() as channel:
        producer = Producer(channel)
        for i in range(12):
            producer.publish({'hello': 'world'},
                             retry=True,
                             exchange=task_queue.exchange,
                             routing_key=task_queue.routing_key,
                             declare=[task_queue])


def get_message(body, message):
    print("receive message: %s" % body)
    # message.ack()


# # 消费者
# with Connection(rabbitmq_url) as conn:
#     with conn.channel() as channel:
#         consumer = Consumer(channel, queues=task_queue, callbacks=[
#                             get_message, ], prefetch_count=10)
#         consumer.consume(no_ack=True)
