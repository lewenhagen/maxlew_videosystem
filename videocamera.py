#!/usr/bin/env python3

import cv2
import numpy as np

class VideoCamera(object):
    def __init__(self, options, resolution="1280x720"):
        self.name = options[0]
        self.ip = options[1]
        self.resolution = resolution
        self.url = "{}/axis-cgi/mjpg/video.cgi?resolution={}&compression=25&camera=1".format(self.ip, self.resolution)
        self.video = cv2.VideoCapture(self.url)
        self.frames = []
        # self.delay = 15
        # self.counter = 0
        # self.fps = 15
        # self.timer = self.delay * self.fps

    def __del__(self):
        self.video.release()

    def release_cam(self):
        self.video.release()

    def get_loading_image(self, counter):
        # print(counter)
        img = cv2.imread('static/img/hourglass/{}.jpg'.format(counter))
        # img = cv2.imread('static/img/hour.jpg')
        ret, jpeg = cv2.imencode('.JPEG', img)
        return jpeg.tobytes()

    def get_frame(self):
        success, image = self.video.read()

        # print(success, image)
        if not success:
            success, image = self.video.read()
        else:
            ret, jpeg = cv2.imencode('.JPEG', image)

        if not ret:
            return

        return jpeg.tobytes()

    def set_quality(self, resolution):
        self.url = "{}/axis-cgi/mjpg/video.cgi?resolution={}&compression=25&camera=1".format(self.ip, resolution)

    def get_name(self):
        return self.name

    def get_url(self):
        return self.url
