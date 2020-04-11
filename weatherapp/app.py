#!/usr/bin/python

""" jocalado | WEATHER APP """

from flask import Flask, request, render_template
import requests
import logging
import os

#write log output to log.log file
logging.basicConfig(format='%(asctime)s-%(process)d-%(levelname)s-%(message)s',filename="log.log", level=logging.INFO)

#instantiate logger
logger = logging.getLogger()

# access values from oracle_credentials
try:
    API_KEY = os.environ['WEATHER_KEY']
except KeyError as e:
    logger.error("Missing environment variables!")
    exit()

app = Flask(__name__)

@app.route('/')
def index():
    return '<h1>Welcome to weather app</h1>'

@app.route('/city')
def search_city():
    city = request.args.get('q')  # city name passed as argument

    # call API and convert response into Python dictionary
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&APPID={API_KEY}'
    response = requests.get(url).json()
    
    # error like unknown city name, invalid api key
    if response.get('cod') != 200:
        message = response.get('message', '')
        return f'Error getting temperature for {city.title()}. Error message = {message}'
    
    # get current temperature and convert it into Celsius
    current_temperature = response.get('main', {}).get('temp')
    if current_temperature:
        current_temperature_celsius = round(current_temperature - 273.15, 2)
        return f'Current temperature of {city.title()} is {current_temperature_celsius} &#8451;'
    else:
        return f'Error getting temperature for {city.title()}'

if __name__ == '__main__':
    #set debug to False when app moves to production
    app.run(debug=True)