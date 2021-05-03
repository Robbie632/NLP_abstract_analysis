
from time import sleep
#rabbitmq details, for set up see https://docs.celeryproject.org/en/latest/getting-started/backends-and-brokers/rabbitmq.html#broker-rabbitmq
#user: user
#password: password
#vhost: myvhost
#tags:mytag

from celery import Celery

app = Celery('app', #name of current module 
            backend='redis://my_redis', #define  backend, redis://<container_name>
          
            broker='amqp://my_rabbit_mq:5672//', #message broker, for rabbitmq use amqp://<container_name>:5672
            )

if __name__ == "__main__":
  app.start()

