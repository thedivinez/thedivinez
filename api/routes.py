from flask import Blueprint
from api.processor import Engine
from flask.globals import request
from flask import render_template as show

web = Blueprint(__name__, "web")


@web.route("/")
def index():
  return show("main.html"), 200


@web.route("/apps/<target>", methods=["GET"])
def gotopage(target):
  return show(f"projects/{target}.html"), 200


@web.route("/<target>", methods=["GET", "POST"])
def decidewhattodo(target):
  func = getattr(Engine, target)
  return func() if request.method == "POST" else show(f"{target}.html", data=func())