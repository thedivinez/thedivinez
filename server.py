from api.routes import web
from config.source import app
from flask_compress import Compress

app.register_blueprint(web)
Compress(app)

if __name__ == "__main__":
  app.run(debug=True)