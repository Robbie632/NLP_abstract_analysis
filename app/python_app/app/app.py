from flask import Flask, render_template, request, redirect, url_for
from form import Form
from dataProcessing.routes import  dataProcess_bp
from celery import Celery
import nltk

#run this in terminal before startin gapp
#export GOOGLE_APPLICATION_CREDENTIALS="/home/user/Documents/semiotic-anvil-253215-cfce3bcf8f4a.json"

app = Flask(__name__)


app.config['SECRET_KEY'] = '15101964'
app.config['CELERY_BROKER_URL'] = 'amqp://my_rabbit_mq:5672//'
app.config['CELERY_RESULT_BACKEND'] = 'redis://my_redis'

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

app.register_blueprint(dataProcess_bp)

@app.route('celeryTest')
def celeryTest():
  task = my_background_test.delay()
  #I get error here due to trying to import my_background_test, 
  #just have a look at the repo associated with the blog post to see where 
  # the "my_background_test" function is stored and how it is imported to
  #solve this problem


if __name__ == "__main__":
    nltk.download('stopwords')
    nltk.download('punkt')
    app.run(host = '0.0.0.0', debug=True, port = 5000)
