import os
from pytz import timezone
from datetime import datetime
from twilio.rest import Client
from tinydb import TinyDB, Query
from flask import request, jsonify
from flask import Flask, render_template

db_query = Query()
table = TinyDB(os.path.join(os.getcwd(), "static", "db", "messages.db")).table("newmessages")

app = Flask(__name__)
app.secret_key = "s-u-p-e-r-s-e-c-r-e-t-k-e-y"


def todaydate():
  now_utc = datetime.now(timezone("UTC"))
  now_africa = now_utc.astimezone(timezone("Africa/Harare"))
  return (now_africa.strftime('%d %b %Y'), now_africa.strftime('%H:%M'))


def sendmeanotification(job):
  auth_token = "bbcda324a4f20c35d8f6a81df44e028a"
  account_sid = "ACc255075c59b5e719afc127c5c8d9437b"
  table.insert(job)
  client = Client(account_sid, auth_token)
  client.messages.create(
      body=f"You have 1 new job offer from {job['name']}. Check it out http://thedivinez.online/jobs",
      from_='+14133388566',
      to='+263786854223')
  return "Thank you for getting in touch, your message has been submited, Divine will get back to you as soon as possible."


@app.route("/")
def index():
  return render_template("main.html")


@app.route("/jobs")
def jobs():
  return render_template("jobs.html", jobs=table.all())


@app.route("/newmessage", methods=["POST"])
def newmesage():
  job = dict(request.form)
  datetimenow = todaydate()
  job["date"] = datetimenow[0]
  job["time"] = datetimenow[1]
  return jsonify({"message": sendmeanotification(job)})


if __name__ == "__main__":
  app.run(debug=True)