from flask import request
from telejoiner.engine.instances import Instances
from flask_socketio import Namespace, join_room, leave_room
from telejoiner.config.source import ServerConfig as task


class TeleJoiner(Namespace, Instances):
    def on_connect(self):
        join_room(request.args["username"]) if request.args["username"] else True
        print(f"=== {request.args['username'] if request.args['username'] else 'new user'} connected ===")

    def on_startjoining(self, account):
        task.run_in_background(self.startjoining, account)

    def on_disconnect(self):
        leave_room(request.args["username"]) if request.args["username"] else True
        print(f"=== {request.args['username'] if request.args['username'] else 'new user'} disconnected ===")