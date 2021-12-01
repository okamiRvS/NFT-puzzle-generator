import os
import cv2
import pdb
import matplotlib.pyplot as plt


class layer():

    def __init__(self, path) -> None:

        self.path = path
        self.img = []
        self.name = []


    def addImg(self, path):

        # PNG images usually have four channels. Three color channels for red, green and blue, and the fourth channel is for transparency, also called alpha channel.
        # The syntax of imread() function contains a second argument whose default value is cv2.IMREAD_COLOR. Any transparency present in the image is not read.
        # To read PNG images with transparency (alpha) channel, use cv2.IMREAD_UNCHANGED as second argument in cv2.imread() function as shown in the following.
        tmp = cv2.imread(path, cv2.IMREAD_UNCHANGED)
        self.img.append(tmp)


    def addName(self, name):

        self.name.append(name)
        

    def show(self):

        for img in self.img:
            self.show(img, 0.3)


    def show(self, img, time):

        fig = plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGBA))
        plt.axis('off')
        fig.axes.get_xaxis().set_visible(False)
        fig.axes.get_yaxis().set_visible(False)
        plt.pause(time)
        plt.clf()