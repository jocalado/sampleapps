#!/usr/bin/python

""" jocalado | NASA APOD API """

from flask import (Flask,render_template)
import yaml
import requests
import logging
import os

#write log output to log.log file
logging.basicConfig(format='%(asctime)s-%(process)d-%(levelname)s-%(message)s',filename="log.log", level=logging.INFO)

#instantiate logger
logger = logging.getLogger()

# access values from oracle_credentials
try:
    email = os.environ['NASA_EMAIL']
    nasakey = os.environ['NASA_KEY']
except KeyError as e:
    logger.error("Missing environment variables!")
    exit()

# Create the application instance
app = Flask(__name__, template_folder="templates")

# Create a URL route in our application for "/"
@app.route('/')
def home():
    """
    This function just responds to the browser ULR
    localhost:5000/

    :return:        the rendered template 'home.html'
    """
    return render_template('home.html')

@app.route('/apod')
def apodtest():
    r = requests.get('https://api.nasa.gov/planetary/apod?api_key='+nasakey)
    return r.text
    #r.status_code

# If we're running in stand alone mode, run the application
if __name__ == '__main__':
    app.run(debug=True)