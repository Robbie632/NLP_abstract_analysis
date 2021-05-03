
#!/usr/bin/env python

from time import sleep
import pika

def send_message():

	#connect to queue, routing_key is the name of the queue and body is the message
	#set up connection, this is causing the problem atm, it cant see the rabbitmq container
	connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', 
                                                                 connection_attempts = 5, 
                                                                 retry_delay = 5))
	#connect
	channel = connection.channel()
	channel_2 = connection.channel()
	#declare a queue called hello, this is what stores messgaes, kind of like a queue
	channel.queue_declare(queue='hello')
	channel_2.queue_declare(queue='hello_there')


	while True:

		#produce messages
		channel.basic_publish(exchange='', 
                          routing_key='hello', # name of queue
                          body='Hello World!') # message content

		channel_2.basic_publish(exchange='', 
                            routing_key='hello_there', 
                            body='Hello World!')

		print(" Sent 'Hello World!'")
		sleep(1)

	#close connection
	connection.close()

if __name__ == '__main__':
	send_message()
