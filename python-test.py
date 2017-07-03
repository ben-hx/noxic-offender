import os
import pyttsx
import requests
from flask import Flask
from flask import jsonify
from flask import json
from random import randint
import pygame
import pygame.camera
import time


class SlackService(object):
    def postImage(self, filename):
        token  = "xoxp-204073677842-204172877269-204332395893-31ba787af2b7646798ec1a6e12da7736"
        channels = "#general"
        media = {'file': (filename, open(filename, 'rb'), 'image/jpg', {'Expires': '0'})}
        response = requests.post(url='https://slack.com/api/files.upload', data=
        {'token': token, 'channels': channels, 'media': media},
                                 headers={'Accept': 'application/json'}, files=media)
        return response.text

    def __init__(self, pictureService):
        self.pictureService = pictureService

    def send(self, text):
        url = "https://hooks.slack.com/services/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"
        params = {
            "text": text,
        }
        headers = {'content-type': 'application/json'}
        r = requests.post(url, json=params, headers=headers)


class TextToSpeech(object):
    def __init__(self, speed=60):
        self.speed = speed

    def speak(self, text):
        engine = pyttsx.init()
        engine.setProperty('voice', 'german')
        engine.setProperty('rate', engine.getProperty('rate') - self.speed)
        engine.say(text)
        engine.runAndWait()


class Offender(object):
    def getRandomOffense(self):
        rails_url = os.path.join(os.path.dirname(os.path.realpath(__file__)), "", "assets/data.json")
        data = json.load(open(rails_url))
        index = randint(0, len(data["rails"]) - 1)
        value = data["rails"][index]
        return value


class PictureService(object):
    def takePicture(self):
        pygame.camera.init()
        pygame.camera.list_cameras()
        cam = pygame.camera.Camera("/dev/video0", (640, 480))
        cam.start()
        time.sleep(0.1)  # You might need something higher in the beginning
        img = cam.get_image()
        pygame.image.save(img, "pygame.jpg")
        cam.stop()
        time.sleep(0.1)
        return "/dev/video0/pygame.jpg"


class Factory(object):
    def __init__(self):
        self.pictureService = PictureService()
        self.textToSpeech = TextToSpeech()
        self.slackService = SlackService(self.pictureService)
        self.offender = Offender()

    def getTextToSpeachInstance(self):
        return self.textToSpeech

    def getSlackServiceInstance(self):
        return self.slackService

    def getOffenderInstance(self):
        return self.offender

    def getPictureServiceInstance(self):
        return self.pictureService


app = Flask(__name__)
factory = Factory()

@app.route('/')
def root():
    offender = factory.getOffenderInstance()
    offense = offender.getRandomOffense()
    textToSpeech = factory.getTextToSpeachInstance()
    textToSpeech.speak(offense)
    slackService = factory.getSlackServiceInstance()
    slackService.send(offense)
    return jsonify(result=offense)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
