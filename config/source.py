import os, pymongo
from dotenv import dotenv_values
from flask_socketio import SocketIO
from flask import Flask, render_template

stc = os.path.join(os.getcwd(), "static")
tmp = os.path.join(os.getcwd(), "templates")
config = dotenv_values(os.path.join(os.getcwd(), ".env"))
app = Flask(__name__, template_folder=tmp, static_folder=stc)
table = pymongo.MongoClient(config.get("MONGO_URL")).thedivinez
#table = pymongo.MongoClient().thedivinez
socket = SocketIO(app)


@app.errorhandler(Exception)
def all_exception_handler(error):
    print(error)
    return render_template('404.html')


def siteconfigs():
    data = {
        "section":
        "portfolio",
        "data": [
            {
                "subsection": "web",
                "title": "COVID-19 SELF-SCREENING BOT",
                "image": "../static/img/portfolio/covidbot.png",
                "link": "https://covidscreen.herokuapp.com"
            },
            {
                "subsection": "web",
                "title": "SPORT SHOES WEBSITE",
                "image": "../static/img/portfolio/sportshoes.jpg",
                "link": "#"
            },
            {
                "subsection": "web",
                "title": "FULLY RESPONSIVE WEBSITE",
                "image": "../static/img/portfolio/responsive.jpg",
                "link": "#"
            },
            {
                "subsection": "mobile",
                "title": "PHOTOCO MOBILE APP",
                "image": "../static/img/portfolio/photoco.jpg",
                "link": "#"
            },
            {
                "subsection": "mobile",
                "title": "CUSTOM SERVICES APP",
                "image": "../static/img/portfolio/servicesapp.jpg",
                "link": "#"
            },
            {
                "subsection": "mobile",
                "subsection": "marketing",
                "title": "DIGITAL MARKETING",
                "image": "../static/img/portfolio/digitalm.jpg",
                "link": "#"
            },
            {
                "subsection": "mobile",
                "title": "MOBILE APP DEVELOPMENT",
                "image": "../static/img/portfolio/appdev.jpg",
                "link": "#"
            },
            {
                "subsection": "web",
                "title": "ART & PHOTOGRAPHY WEBSITE",
                "image": "../static/img/portfolio/art.jpg",
                "link": "#"
            },
            {
                "subsection": "web",
                "title": "DOCTOR MANAGEMENT WEBSITE",
                "image": "../static/img/portfolio/doctor.png",
                "link": "#"
            },
        ]
    }
    table.configs.delete_many({})
    table.configs.insert_one(data)
    portfoliodata = table.configs.find_one({"section": "portfolio"}, {"_id": 0})
    print(portfoliodata)
