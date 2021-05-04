from flask import Flask, render_template, request, redirect, url_for, flash
from form import Form
from dataProcessing.routes import  dataProcess_bp
from celery import Celery
import nltk
from time import sleep

#run this in terminal before startin gapp
#export GOOGLE_APPLICATION_CREDENTIALS="/home/user/Documents/semiotic-anvil-253215-cfce3bcf8f4a.json"

app = Flask(__name__)


app.config['SECRET_KEY'] = '15101964'
app.config['CELERY_BROKER_URL'] = 'amqp://my_rabbit_mq:5672//'
app.config['CELERY_RESULT_BACKEND'] = 'redis://my_redis'

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

app.register_blueprint(dataProcess_bp)

@app.route('/celeryTest')
def celeryTest():
  task = my_background_test.delay()

  # question
  # how do I access the returned "result" of my_background_test() when it's ready
  # how do I check the status?

  # answer
  # web page running in your browser uses ajax to poll the server for 
  # status updates on all these tasks. For each task the page will 
  # show a graphical status bar, a completion percentage, a status message, 
  # and when the task completes, a result value will be shown as well.

  # the flashed message will be available in the rendered html 
  flash("my_background test function has just been sent for processing async style")


  return redirect(url_for('async_landing'))

@app.route('/async_landing')
def async_landing():

  return render_template("async_landing.html")

@celery.task
def my_background_test():
  sleep(5)
  return("result")


if __name__ == "__main__":
    nltk.download('stopwords')
    nltk.download('punkt')
    app.run(host = '0.0.0.0', debug=True, port = 5000)
