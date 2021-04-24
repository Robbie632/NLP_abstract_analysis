from flask import Flask, render_template, request, redirect, url_for
from form import Form
from dataProcessing.routes import  dataProcess_bp


app = Flask(__name__)

app.config['SECRET_KEY'] = '15101964'

app.register_blueprint(dataProcess_bp)

if __name__ == "__main__":
    app.run(debug=True)
