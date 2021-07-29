from flask_cors import CORS
from config.source import app
from api.main.routes import web
from flask_compress import Compress
from config.source import app, socket
from api.telejoiner.main import TeleJoiner

app.register_blueprint(web)

CORS(app)
Compress(app)
socket.on_namespace(TeleJoiner(namespace="/telejoiner"))

# === start the server ===
if __name__ == "__main__":
    socket.run(app, debug=True)
