from flask import *
from fileinput import filename
import os
from sage_converter import sage_start

app = Flask(__name__)



@app.route("/")
def hello_world():
        return render_template("index.html")

@app.route("/upload", methods = ['POST'])
def upload():
        if request.method == "POST":
                f  =request.files['file']
                f.save(f.filename)
                print(f.filename)
                sage_start(f.filename,"Conversion")
        return render_template("index.html")

if __name__ == "__main__":
        app.run(host="0.0.0.0")