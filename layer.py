import os
import cv2
import pdb
import matplotlib.pyplot as plt
import numpy as np


class layer():

    def __init__(self, path) -> None:

        self.path = path
        self.img = []
        self.name = []

        self.rarity = []
        self.normal = 0
        self.rare = 0
        self.ultrarare = 0

        self.probNormal = 0.7
        self.probRare = 0.25
        self.probUltraRare = 0.05

        self.isComplexLayer = False
        self.index = -1
        self.foreground = None


    def addImg(self, path):

        # PNG images usually have four channels. Three color channels for red, green and blue, and the fourth channel is for transparency, also called alpha channel.
        # The syntax of imread() function contains a second argument whose default value is cv2.IMREAD_COLOR. Any transparency present in the image is not read.
        # To read PNG images with transparency (alpha) channel, use cv2.IMREAD_UNCHANGED as second argument in cv2.imread() function as shown in the following.
        tmp = cv2.imread(path, cv2.IMREAD_UNCHANGED)
        self.img.append(tmp)


    def addBlanckImg(self, width, height):
        
        # add blank image
        tmp = np.zeros([width, height, 4], dtype=np.uint8)
        self.img.append(tmp)


    def addNameAndRarity(self, name):

        x = name.find("_SSS")
        y = name.find("_SS")
        if x > 0:
            self.ultrarare+=1
            self.rarity.append("ultrarare")
        elif y > 0:
            self.rare+=1
            self.rarity.append("rare")
        else:
            self.normal+=1
            self.rarity.append("normal") # no obj is trated like a normal obj

        self.name.append(name)
    

    def computeWeight(self):

        if self.normal == 0:
            singleProbNormal = 0
        else:
            singleProbNormal = self.probNormal / self.normal

        if self.rare == 0:
            singleProbRare = 0
        else:
            singleProbRare = self.probRare / self.rare

        if self.ultrarare == 0:
            singleProbUltraRare = 0
        else:
            singleProbUltraRare = self.probUltraRare / self.ultrarare

        for i in range(len(self.rarity)):
            if self.rarity[i] == "normal":
                self.rarity[i] = singleProbNormal
            elif self.rarity[i] == "rare":
                self.rarity[i] = singleProbRare
            else:
                self.rarity[i] = singleProbUltraRare
        
        # normalize array in this way sum is 1
        self.rarity = self.rarity / np.sum(self.rarity)


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