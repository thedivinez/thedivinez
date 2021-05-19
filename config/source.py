import os, pymongo
from dotenv import dotenv_values
from flask_compress import Compress
from flask import Flask, render_template

stc = os.path.join(os.getcwd(), "static")
tmp = os.path.join(os.getcwd(), "templates")
config = dotenv_values(os.path.join(os.getcwd(), ".env"))
app = Flask(__name__, template_folder=tmp, static_folder=stc)
table = pymongo.MongoClient(config.get("MONGO_URL")).thedivinez

Compress(app)


@app.errorhandler(Exception)
def all_exception_handler(error):
  return render_template('404.html')