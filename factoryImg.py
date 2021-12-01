import os
import cv2
import pdb
import matplotlib.pyplot as plt
import layer as ly
import random
import copy
import factoryJson as fJson
import puzzle as puzz
import json
import hashlib
import datetime

class factoryImg():

    def __init__(self, currentDir, layersName) -> None:

        layers = []

        root = "layers"
        
        for dir in layersName:
            pathDir = os.path.join(root, dir)
            print(pathDir)

            layers.append(ly.layer(dir))

            files = os.listdir(pathDir)

            for file in files:

                pathImg = os.path.join(pathDir, file)

                layers[-1].addName(file)
                layers[-1].addImg(pathImg)

        self.layersName = layersName

        self.layers = layers

        self.currentImg = -1

        self.imgFolder = "imgs"

        self.fJson = fJson.factoryJson()

        self.puzz = puzz.puzzle()


    def showAllImgs(self):
                
        for layer in self.layers:
            layer.show()


    def generateRandomImg(self):

        elements = []

        # list with all index of layer choosen randomly
        randDecision = []

        # list with all information about each layer choosen
        attributes = []

        for i, layer in enumerate(self.layers):
            # random.randint(0, 10) will return
            # a random number from [0, 1, 2, 3, 4, 5, 6, 7, 8 ,9, 10]
            if len(layer.img)-1 == 0:
                num = 0

            else:
                num = random.randint(0, len(layer.img)-1)
                #print(num)

            # save data for the json            
            '''
            # SAVE A
            randDecision.append({f"{i}": num})
            attributes.append({
                "id": i,
                "layer": layer.path,
                "name": layer.name[num],
                "rarity": "rare"
            })
            '''

            # SAVE B
            randDecision.append({f"{i}": num})
            attributes.append({
                "trait_type": layer.path,
                "value": layer.name[num]
            })     


            elements.append(copy.deepcopy(layer.img[num]))

        background = elements[-1]
        for element in elements[::-1][1::]:
            foreground = element
            
            # normalize alpha channels from 0-255 to 0-1
            alpha_background = background[:,:,3] / 255.0
            alpha_foreground = foreground[:,:,3] / 255.0

            # set adjusted colors
            for color in range(0, 3):
                background[:,:,color] = alpha_foreground * foreground[:,:,color] + \
                    alpha_background * background[:,:,color] * (1 - alpha_foreground)

            # set adjusted alpha and denormalize back to 0-255
            background[:,:,3] = (1 - (1 - alpha_foreground) * (1 - alpha_background)) * 255

        # display the image
        #layer.show(background, 0.1)

        data = self.fJson.buildJson(randDecision, attributes, self.currentImg)
        self.fJson.createSingleJson(self.imgFolder, self.currentImg)


        return background


    def generateRandomPuzzle(self):

        randIMG = self.generateRandomImg()
        imgPuzzle = self.puzz.puzzling(randIMG)

        return randIMG, imgPuzzle


    def createDir(self, path):

        if not os.path.exists(path):
            if os.name == 'posix': # if linux system
                os.system(f"mkdir -p {path}")
            if os.name == 'nt': # if windows system
                os.system(f"mkdir {path}")


    def RandomImgs(self, number):

        tmpImgs = os.path.join(self.imgFolder)
        self.createDir(tmpImgs)

        for i in range(number):
            self.currentImg = i
            randIMG, imgPuzzle = self.generateRandomPuzzle()

            imgPath = os.path.join(tmpImgs, f"{i}.png")
            print(imgPath)
            cv2.imwrite(imgPath, randIMG) # saveImg

            dirPuzzle = os.path.join(tmpImgs, str(i))
            self.createDir(dirPuzzle)

            # save 9 piecies of puzzle
            for idx, imPuz in enumerate(imgPuzzle):
                imgPuzPath = os.path.join(dirPuzzle, f"{idx}.png")
                self.fJson.createPuzzleJson(self.imgFolder, self.currentImg)
                cv2.imwrite(imgPuzPath, imPuz)
    
        self.fJson.createMetaDataJson(self.imgFolder)