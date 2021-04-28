import os
from tinydb import TinyDB, Query
from flask import request, jsonify
from flask import Flask, render_template

db_query = Query()
table = TinyDB(os.path.join(os.getcwd(), "static", "db", "messages.db")).table("newmessages")

app = Flask(__name__)


@app.route("/")
def index():
  return render_template("main.html")


@app.route("/newmessage", methods=["GET"])
def newmesage():
  table.insert(request.form)
  return jsonify({"status": True})


if __name__ == "__main__":
  app.run(debug=True)