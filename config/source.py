import os, pymongo
from dotenv import dotenv_values
from flask import Flask, render_template, json

stc = os.path.join(os.getcwd(), "static")
tmp = os.path.join(os.getcwd(), "templates")
config = dotenv_values(os.path.join(os.getcwd(), ".env"))
app = Flask(__name__, template_folder=tmp, static_folder=stc)
thedivinez_db = pymongo.MongoClient(config.get("MONGO_URL")).thedivinez


@app.errorhandler(Exception)
def all_exception_handler(error):
    print(error)
    return render_template('404.html')


class ServerConfig:
    @staticmethod
    def siteconfigs():
        data = json.load(open(os.path.join(os.getcwd(), "config", "pages.json")))
        thedivinez_db.configs.delete_many({})
        thedivinez_db.configs.insert_one(data)
        thedivinez_db.configs.find_one({"section": "portfolio"}, {"_id": 0})
