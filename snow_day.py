#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 28 12:38:59 2016

@author: matthewbarcus
"""

from flask import Flask
from flask_ask import Ask, statement, question, session
import bs4 as bs
import urllib.request


app = Flask(__name__)
ask = Ask(app, "/snowday")

def get_weather():
    sauce = urllib.request.urlopen('http://www.weny.com/school-closings').read()
    soup = bs.BeautifulSoup(sauce, 'lxml')
    status = [span.text for span in soup.find_all('span', 
                                                         class_='closing-title')]
    status = [i.strip() for i in status]
    
    if status[0] == 'No cancellations or closings.':
        weather = status[0]
    else:
        result = [span.text for span in soup.find_all('span', 
                                                         class_='closing-status1')]
        status = [(status[i], result[i]) for i in range(len(status))]
        last_update = [paragraph.string for paragraph in soup.find_all('div', 
                                                                   class_='closing-content subpend-1 bold')][0]
        weather = 'As of %s...' %(last_update.split(': ')[1])
        for i in range(len(status)):
            weather += '%s ... %s ...' %(status[i][0],status[i][1])    
    return weather
    
@app.route("/")
def homepage():
    weather = get_weather()
    report = "Today's report is: {}".format(weather)
    return report
    #return "Snow Day skill for ALEXA"
   

@ask.launch
def start_skill():
    weather = get_weather()
    report = "Today's report is: {}".format(weather)
    return statement(report)
    
@ask.intent("YesIntent")
def share_weather():
    weather = get_weather()
    report = "Today's report is: {}".format(weather)
    return statement(report)
    
@ask.intent("NoIntent")
def no_intent():
    bye = 'Thank you, come again'
    return question(bye)

    
if __name__ == '__main__':
    app.run(debug=True)
    