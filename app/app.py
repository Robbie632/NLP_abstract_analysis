from flask import Flask, render_template, request, redirect, url_for
from form import Form
import os
import sys
import cv2
sys.path.append("..")
from utils import ClusterAbstract, MyKMeans




app = Flask(__name__)

app.config['SECRET_KEY'] = '15101964'



@app.route('/', methods=["GET", "POST"])
def form():
  form = Form()
  if form.is_submitted():
     #retrieve entered text
    answer = form.question.data
    ca = ClusterAbstract()
    ca.get(answer, #keyword query
          '5'#number of abstracts
      )
    ca.process_data()
    ca.encode_data()
    ca.cluster_data(3)

    ca.analyse_clusters()

    ca.generate_word_clouds()
    print(f"clusters are {ca.model.labels}")

    #run cluster analysis
    print(type(ca.word_clouds[0]))
    filenames_list = []
    for c, img in enumerate(ca.word_clouds):
      filenames_list.append(f"wordcloud_{c}.png")
      img.to_file(os.path.join("static", f"wordcloud_{c}.png"))


 

    return render_template("landing.html", filenames_list=filenames_list)


  else:
    return render_template("ask.html", form=form)

@app.route('/landing', methods=["GET", "POST"])
def landing():
  return render_template("landing.html")


if __name__ == "__main__":
    app.run(debug=True)
