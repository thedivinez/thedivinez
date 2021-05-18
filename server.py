import pymongo
from pytz import timezone
from datetime import datetime
from twilio.rest import Client
from flask import request, jsonify
from flask import Flask, render_template

app = Flask(__name__)
app.secret_key = "s-u-p-e-r-s-e-c-r-e-t-k-e-y"
connection = f"mongodb+srv://divine01:imwinning@splitcluster.aui7k.azure.mongodb.net/thedivinez?retryWrites=true&w=majority"
table = pymongo.MongoClient(connection).thedivinez


def todaydate():
  now_utc = datetime.now(timezone("UTC"))
  now_africa = now_utc.astimezone(timezone("Africa/Harare"))
  return (now_africa.strftime('%d %b %Y'), now_africa.strftime('%H:%M'))


def sendmeanotification(job):
  table.jobs.insert_one(job)
  auth_token = "bbcda324a4f20c35d8f6a81df44e028a"
  account_sid = "ACc255075c59b5e719afc127c5c8d9437b"
  client = Client(account_sid, auth_token)
  client.messages.create(body=f"You have 1 new job offer from {job['name']} ~ {job['email']}",
                         from_='+14133388566',
                         to='+263786854223')
  return f"Thank you {job['name']} for getting in touch, Divine will get back to you as soon as possible."


@app.route("/")
def index():
  return render_template("main.html")


@app.route("/jobs")
def jobs():
  return render_template("jobs.html", jobs=list(table.jobs.find({}, {"_id": 0})))


@app.route("/apps/<target>")
def gotopage(target):
  return render_template(f"projects/{target}.html")


@app.route("/newmessage", methods=["POST"])
def newmesage():
  job = dict(request.form)
  datetimenow = todaydate()
  job["date"] = datetimenow[0]
  job["time"] = datetimenow[1]
  return jsonify({"message": sendmeanotification(job)})


if __name__ == "__main__":
  app.run(debug=True)