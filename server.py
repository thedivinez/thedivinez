from api.routes import web
from flask_cors import CORS
from config.source import app
from flask_compress import Compress

app.register_blueprint(web)

# === allow cross origin ===
CORS(app)

#=== compress the server ===
Compress(app)
# === start the server ===
if __name__ == "__main__":
  app.run(debug=True)