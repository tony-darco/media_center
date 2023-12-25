import logging
import json

config_file = open("support.json")
config_data = json.load(config_file)

log_file = config_data["media_config"]["log_file"]
file_types_list = config_data["media_config"]["file_types_list"]

logging.basicConfig(filename=log_file, level=logging.DEBUG,filemode='a', format='%(asctime)s: %(levelname)s - %(message)s')

from flask import *
from fileinput import filename
import os
from image_center import image_start

app = Flask(__name__)

INPUT_DIR = "staging/"
OUTPUT_DIR = "backstage/"


img = os.path.join('static','Image')

@app.errorhandler(500)
def internal_error(error):
    return(render_template('error_pages/500.html'),500)

@app.errorhandler(404)
def internal_error(error):
    return(render_template('error_pages/404.html'),404)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/formats")
def formats():
    list_of_support = []
    with open(file_types_list, "r") as file_support:
        lines = file_support.readlines()
        for i in lines:
            list_of_support.append(i)
    return render_template("formats.html",supported_types=list_of_support)

@app.route("/media_center")
def imageService():
    return render_template("index1.html")

@app.route("/image_center")
def image_center():
    return render_template("image_center.html")

@app.route("/audio_center")
def audio_center():
    return render_template("audio_center.html")

@app.route("/video_center")
def video_center():
    return render_template("video_center.html")

@app.route("/upload", methods = ['GET','POST'])
def upload():
    if request.method == "POST":
        f  =request.files['file']
        f.save(INPUT_DIR+f.filename)
        
        image_file_path = image_start(f.filename,request.form)
            
    return render_template("output.html", image_path = image_file_path)

if __name__ == "__main__":
    app.run(host="127.0.0.1", debug=True)