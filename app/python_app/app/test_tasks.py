from app import celery
from time import sleep

@celery.task

def my_background_test():
  sleep(5)

  return("result")
