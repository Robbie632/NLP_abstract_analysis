from flask import Blueprint, render_template
from form import Form
import sys
import os
import time
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
    keyword = form.question.data
    n_clusters = int(form.clusters.data)
    n_abstracts = form.abstracts.data

    ca = ClusterAbstract()
    ca.run(keyword, n_abstracts, n_clusters)

    filenames_list = []
  
    for c, img in enumerate(ca.word_clouds):
      t = str(time.time()).replace('.', '_')
      f = f"wordcloud_{c}_{t}.png"
      filenames_list.append(f)

      #the path below has to be absolute because the path 
      # used by the Dockerfile may be different
      img.to_file(os.path.join("/app/app/static", f))
   

    return render_template("landing.html", filenames_list=filenames_list)

  else:
    return render_template("ask.html", form=form)

