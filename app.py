from flask import *
from fileinput import filename
import os
from sage_converter import sage_start

app = Flask(__name__)

INPUTDIR = "staging/"
OUTDIR = "backstage/"

img = os.path.join('static','Image')

@app.route("/")
def hello_world():
        return render_template("index.html")

@app.route("/upload", methods = ['POST'])
def upload():
        if request.method == "POST":
                f  =request.files['file']
                f.save(INPUTDIR+f.filename)
                
                image_file_path = sage_start(f.filename,request.form)
                
        return render_template("output.html", image_path = image_file_path)

if __name__ == "__main__":
        app.run(host="0.0.0.0", debug=True)