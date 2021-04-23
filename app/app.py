from flask import Flask, render_template, request, redirect, url_for
from form import Form
import os
import sys
import cv2
sys.path.append("..")

from utils import ClusterAbstract, MyKMeans

import matplotlib.pyplot as plt, mpld3


app = Flask(__name__)

app.config['SECRET_KEY'] = '15101964'



@app.route('/', methods=["GET", "POST"])
def form():
  form = Form()
  if form.is_submitted():

    # #retrieve entered text
    # answer = form.question.data

    # #clustering
    # ca = ClusterAbstract()
    # ca.get(answer, #keyword query
    #      '5'#number of abstracts
    #   )
    # ca.process_data()
    # ca.encode_data()
    # ca.cluster_data(3)

    # ca.analyse_clusters()
  
    # ca.generate_word_clouds()
    # print(f"clusters are {ca.model.labels}")

    # #run cluster analysis
    # print(type(ca.word_clouds[0]))

    # ca.word_clouds[0].to_file("test.png")
    img_pth = "test.png"
    #img_pth = os.path.join("static", img_pth)
    
    print(os.getcwd())

    return redirect(url_for("landing", img_pth=img_pth))


  else:
    return render_template("ask.html", form=form)

@app.route('/landing', methods=["GET", "POST"])
def landing():
  return render_template("landing.html")

import cv2
import base64

def ndarray_to_b64(ndarray):
    """
    converts a np ndarray to a b64 string readable by html-img tags 
    """
    img = cv2.cvtColor(ndarray, cv2.COLOR_RGB2BGR)
    _, buffer = cv2.imencode('.png', img)
    return base64.b64encode(buffer).decode('utf-8')


if __name__ == "__main__":
    app.run(debug=True)
