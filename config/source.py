from functools import wraps
from dotenv import dotenv_values
from flask_socketio import SocketIO
import os, asyncio, pymongo, threading
from flask import Flask, render_template, json

stc = os.path.join(os.getcwd(), "static")
tmp = os.path.join(os.getcwd(), "templates")
config = dotenv_values(os.path.join(os.getcwd(), ".env"))
app = Flask(__name__, template_folder=tmp, static_folder=stc)
telescap_db = pymongo.MongoClient(config.get("MONGO_URL")).telescap
thedivinez_db = pymongo.MongoClient(config.get("MONGO_URL")).thedivinez
socket = SocketIO(app)
socket.init_app(app, cors_allowed_origins="*")


@app.errorhandler(Exception)
def all_exception_handler(error):
    print(error)
    return render_template('404.html')


class ServerConfig:
    @staticmethod
    def sendlogs(username, message):
        """send logs to the client making sure they stay updated"""
        print(message)
        socket.emit("process_status", message, room=username, namespace="/telejoiner")

    @staticmethod
    def asynchronous(function):
        """creates an eventloop for incoming requests or reuses existing event loop"""
        @wraps(function)
        def wrapped(*args, **kwargs):
            try:
                loop = asyncio.get_running_loop()
                print(">> using existing event loop <<")
                return loop.create_task(function(*args, **kwargs))
            except RuntimeError:
                print(">> creating new event loop <<")
                return asyncio.run(function(*args, **kwargs))

        return wrapped

    @staticmethod
    def run_in_background(function, *args, **kwargs):
        """creates a background task on a seperate thread enabling concurrency"""
        threading.Thread(target=function, args=args, kwargs=kwargs).start()

    @staticmethod
    def siteconfigs():
        data = json.loads(open(os.path.join(os.getcwd(), "config", "pages.json")))
        thedivinez_db.configs.delete_many({})
        thedivinez_db.configs.insert_one(data)
        portfoliodata = thedivinez_db.configs.find_one({"section": "portfolio"}, {"_id": 0})
        print(portfoliodata)
