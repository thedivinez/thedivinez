from pytz import timezone
from datetime import datetime
from twilio.rest import Client
from config.source import table
from flask import request, jsonify


class Engine:
  def messages():
    return list(table.messages.find({}, {"_id": 0}))

  def store():
    return {}

  def newmessage():
    message = dict(request.form)
    datetimenow = Engine.todaydate()
    message["date"] = datetimenow.get("date")
    message["time"] = datetimenow.get("time")
    return jsonify({"message": Engine.notify_me(message)})

  def todaydate():
    now_utc = datetime.now(timezone("UTC"))
    now_africa = now_utc.astimezone(timezone("Africa/Harare"))
    return {"date": now_africa.strftime('%d %b %Y'), "time": now_africa.strftime('%H:%M')}

  def createsale():
    sale = dict(request.form)
    datetimenow = Engine.todaydate()
    sale["date"] = datetimenow.get("date")
    sale["time"] = datetimenow.get("time")
    table.sales.insert_one(sale)  # add to db
    return jsonify({"message": "Request submitted. Divine will get back to you as as possibe."})

  def notify_me(msg: dict):
    table.messages.insert_one(msg)
    auth_token = "bbcda324a4f20c35d8f6a81df44e028a"
    client = Client("ACc255075c59b5e719afc127c5c8d9437b", auth_token)
    message = f"1 new message from {msg.get('name')} ~ {msg.get('email')}"
    client.messages.create(body=message, from_='+14133388566', to='+263786854223')
    return f"Thank you {msg['name']} for getting in touch, Divine will get back to you as soon as possible."