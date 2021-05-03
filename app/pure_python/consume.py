#!/usr/bin/env python
import pika
from time import sleep


def consume():
	#set up connection

	connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', 
                                                                 connection_attempts = 5, 
                                                                 retry_delay = 5))

	#connect
	channel = connection.channel()

	#name queue to be connected to, still declare if already been declared by producer
	channel.queue_declare(queue='hello')

	#create callback function, this is executed when a message is received
	def callback(ch, method, properties, body):

		sleep(15)
		with open('output_1.txt', 'a') as f:

      #acknowledge the message
			ch.basic_ack(delivery_tag = method.delivery_tag)

			f.write('received message')
			f.write('\n')

			#the body variable is the message
	    #can do main work here, for example building model



	#set up consumer
	channel.basic_consume(queue='hello', 
                        on_message_callback=callback)

	#wait for messages
	print(' [*] Waiting for messages. To exit press CTRL+C')
	channel.start_consuming()#!/usr/bin/env python


if __name__ == '__main__':
	consume()
