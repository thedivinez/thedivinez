import asyncio, os
import pymongo, threading
from functools import wraps
from dotenv import dotenv_values
from config.source import socket

config = dotenv_values(os.path.join(os.getcwd(), ".env"))
dbcursor = pymongo.MongoClient(config.get("MONGO_URL")).telescap


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