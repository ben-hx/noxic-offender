import os
import pyttsx
from flask import Flask
from flask import jsonify
from flask import json
from random import randint
import win32com.client as wincl

class TextToSpeechLinux(object):
    def __init__(self, pyttsx):
        self.engine = pyttsx.init()
        self.voices = self.engine.getProperty('voices')
        self.engine.setPropperty('voice', 'german')
        self.engine.setProperty('rate', self.engine.getProperty('rate') - 60)

    def speak(self, text):
        self.engine.say(text)
        self.engine.runAndWait()


class TextToSpeechWindows(object):
    def speak(self, text):
        result = wincl.Dispatch("SAPI.SpVoice")
        result.Speak(text)


class Factory(object):
    def getTextToSpeachInstance(self):
        return TextToSpeechWindows()


app = Flask(__name__)
factory = Factory()


def sayAndResponse(value):
    textToSpeech = factory.getTextToSpeachInstance()
    textToSpeech.speak(value)
    return jsonify(result=value)

def getRandomRail():
    rails_url = os.path.join(os.path.dirname(os.path.realpath(__file__)), "", "assets/data.json")
    data = json.load(open(rails_url))
    index = randint(0, len(data["rails"]) - 1)
    # print index
    value = data["rails"][index]
    return value


@app.route('/')
def root():
    result = sayAndResponse(getRandomRail())
    return result

if __name__ == '__main__':
    app.run()
