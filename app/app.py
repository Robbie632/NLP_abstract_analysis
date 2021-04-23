from flask import Flask, render_template, request, redirect, url_for
from form import Form


app = Flask(__name__)

app.config['SECRET_KEY'] = '15101964'



@app.route('/', methods=["GET", "POST"])
def form():
  form = Form()
  if form.is_submitted():
    answer = form.question.data
    return redirect(url_for("landing"))


  else:
    return render_template("ask.html", form=form)

@app.route('/landing', methods=["GET", "POST"])
def landing():
  return render_template("landing.html")


if __name__ == "__main__":
    app.run(debug=True)
