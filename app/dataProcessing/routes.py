from flask import Blueprint, render_template
from form import Form
import sys
import os
sys.path.append("..")

from utils import ClusterAbstract, MyKMeans

dataProcess_bp=Blueprint(
		'dataProcess_bp', 
		__name__,
		template_folder='templates',
		static_folder='static'
		)

@dataProcess_bp.route('/', methods=["GET", "POST"])
def dataProcess():

  """
  route for loading form and processing inputted data
  uses kmeans model to cluster data then creates and 
  renders wordclouds of each clusters' most numerous words
  """

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

