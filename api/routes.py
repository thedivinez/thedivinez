from config.source import table
from api.processor import Engine
from os import path, walk, getcwd
from flask import Blueprint, request
from flask import render_template as show

web = Blueprint(__name__, "web")


@web.route("/")
def index():
  portfoliodata = table.configs.find_one({"section": "portfolio"}, {"_id": 0})
  return show("main.html", portfoliodata=portfoliodata.get("portfolio")), 200


@web.route("/apps/<target>", methods=["GET"])
def gotopage(target):
  return show(f"projects/{target}.html"), 200


@web.route("/<target>", methods=["GET", "POST"])
def decidewhattodo(target):
  func = getattr(Engine, target)
  return func() if request.method == "POST" else show(f"{target}.html", data=func())