from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler

import core
import atexit

application = Flask(__name__)

@application.route("/")
def index():
    return """« Transmettez de moi ne serait-ce qu'un seul verset et rapportez également des enfants d'Israël, il n'y a pas de mal. 
    Quant à celui qui ment délibérément à mon sujet, qu'il se prépare à prendre sa place en Enfer. »"""

def job():
    try:
        core.launcher()
        print("Tweet envoyé avec succès !")
    except:
        print("Le Tweet n'a pas pu être envoyé.")

scheduler = BackgroundScheduler()
# set the interval between the publication of tweets
scheduler.add_job(func=job, trigger="interval", minutes=360)
scheduler.start()

atexit.register(lambda: scheduler.shutdown())

if __name__ == "__main__":
    application.run(port=5000, debug=True)