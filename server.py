from api.routes import web
from config.source import app

app.register_blueprint(web)

if __name__ == "__main__":
  app.run(debug=True)