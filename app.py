from flask import *
from fileinput import filename
import os
from sage_converter import sage_start
import logging

app = Flask(__name__)

INPUTDIR = "staging/"
OUTDIR = "backstage/"

app.logger.setLevel(logging.INFO)
handler = logging.FileHandler("app.log")
app.logger.addHandler(handler)

img = os.path.join('static','Image')

@app.route("/")
def hello_world():
        return render_template("index.html")

@app.route("/upload", methods = ['GET','POST'])
def upload():
    if request.method == "POST":
        f  =request.files['file']
        f.save(INPUTDIR+f.filename)
        
        image_file_path = sage_start(f.filename,request.form)
            
    return render_template("output.html", image_path = image_file_path)

if __name__ == "__main__":
    app.run(host="127.0.0.1", debug=True)