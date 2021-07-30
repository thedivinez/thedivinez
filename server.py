from os import getcwd
from flask import request
from main.processor import Engine
from config.source import app, socket
from telejoiner.main import TeleJoiner
from config.source import thedivinez_db
from flask import render_template as show

socket.on_namespace(TeleJoiner(namespace="/telejoiner"))


@app.route("/")
def index():
    portfoliodata = thedivinez_db.configs.find_one({"section": "portfolio"}, {"_id": 0})
    return show("main.html", portfoliodata=portfoliodata.get("data")), 200


@app.route("/apps/<target>", methods=["GET"])
def gotopage(target):
    return show(f"projects/{target}.html"), 200


@app.route("/<target>", methods=["GET", "POST"])
def decidewhattodo(target):
    func = getattr(Engine, target) if not target == "favicon.ico" else getcwd
    return func() if request.method == "POST" else show(f"{target}.html", data=func())


# === start the server ===
if __name__ == "__main__":
    socket.run(app, debug=True)
