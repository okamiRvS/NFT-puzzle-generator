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
import numpy as np


class factoryImg():

    def __init__(self, currentDir, layersData, width, height, numberImgs) -> None:

        layers = []

        root = "layers"
        
        layersName = list(layersData)

        for idx, dir in enumerate(layersName):
            pathDir = os.path.join(root, dir)
            print(pathDir)

            layers.append(ly.layer(dir))

            files = os.listdir(pathDir)

            for file in files:
                pathImg = os.path.join(pathDir, file)

                layers[-1].addNameAndRarity(file)
                layers[-1].addImg(pathImg)
            
            # if it must not exist then add blanck layer
            if not layersData[dir][0]:
                layers[-1].addNameAndRarity("noObj")
                layers[-1].addBlanckImg(width, height)

            # this means that it is a complex layer with a foreground
            if len(layersData[dir]) > 1:
                # set the current layer ad complex layer
                layers[-1].isComplexLayer = True

                # ...so compute image index of the foreground folder
                index = layersName.index(layersData[dir][1][1])+1
                layers[-1].index = index

                # create foreground layer and add imgs
                nameLayer = layersData[dir][1][0]
                pathDirForeground = os.path.join(root, nameLayer)
                foregroundLayer = ly.layer(pathDirForeground)

                files = os.listdir(pathDirForeground)

                # add imgs into the foregroundLayer
                for file in files:
                    pathImg = os.path.join(pathDirForeground, file)

                    foregroundLayer.addNameAndRarity(file)
                    foregroundLayer.addImg(pathImg)

                # if it must not exist then add blanck layer
                if not layersData[dir][0]:
                    foregroundLayer.addNameAndRarity("noObj")
                    foregroundLayer.addBlanckImg(width, height)

                layers[-1].foreground = foregroundLayer

            layers[-1].computeWeight()

        self.layersName = layersName

        self.layers = layers

        self.currentImg = -1

        self.imgFolder = "imgs"

        self.fJson = fJson.factoryJson()

        self.puzz = puzz.puzzle()

        self.DNAs = []

        self.width = width

        self.height = height

        self.rarityImg = np.zeros(numberImgs, dtype=np.float32)


    def showAllImgs(self):
                
        for layer in self.layers:
            layer.show()


    def verifyUniqueness(self, dna):

        # Verify that this is the unique image
        for d in self.DNAs:
            if np.array_equal(d, dna):
                print(f"Two DNA are the same: {d}")
                return False
        
        return True


    def memorizeRarityImg(self, dna):

        sumV = 0
        for i, val in enumerate(dna):
            sumV += self.layers[i].rarity[val]

        self.rarityImg[self.currentImg] = sumV


    def generateRandomImg(self):

        # list with all index of layer choosen randomly
        dna = np.zeros(len(self.layers), dtype=np.int32)

        # list of the imgs choosen
        elements = []

        # list with all information about each layer choosen
        attributes = []

        condition = True
        while(condition):
            for i, layer in enumerate(self.layers):

                # random.randint(0, 10) will return
                # a random number from [0, 1, 2, 3, 4, 5, 6, 7, 8 ,9, 10]
                if len(layer.img)-1 == 0:
                    num = 0
                else:
                    # https://stackoverflow.com/questions/3679694/a-weighted-version-of-random-choice
                    # count normal and rare in a single layer, I know that I want to assign 0.1 weight for
                    # rare and 0.9 for the normal. So, for example 2 rare and 10 normal, so 0.1/2=0.05 for
                    # each rarity and 0.9/10=0.09 for each normal obj.
                    # if we want rarity each 500imgs then 1/500=0.002 prob assigned to all rare objs of a single layer
                    #num = random.randint(0, len(layer.img)-1)

                    num = random.choices(
                        population=np.arange( len(layer.img) ),
                        weights=layer.rarity,
                        k = 1    
                    )

                if type(num) != int:
                    num = num[0] # extract result

                # save data for the json            
                dna[i] = num

                attributes.append({
                    "trait_type": layer.path,
                    "value": layer.name[num]
                })     
                elements.append(copy.deepcopy(layer.img[num]))

            if self.verifyUniqueness(dna):
                # add dna into the list, because it's valid
                self.DNAs.append(dna)

                # exit from while cycle
                condition = False
            else:
                # reset everything, because it already exists an image with that dna
                dna = np.zeros_like(dna)
                elements = []
                attributes = []

            # manage elements list, not dna because it doesn't change anything there
            for i, layer in enumerate(self.layers):
                if layer.isComplexLayer:
                    valChoosen = dna[i]
                    elements.insert(layer.index, layer.foreground.img[valChoosen])

        self.memorizeRarityImg(dna)

        img = self.createImg(elements)

        data = self.fJson.buildJson(dna, attributes, self.currentImg)
        self.fJson.createSingleJson(self.imgFolder, self.currentImg)

        return img


    def createImg(self, elements):

        # create the image
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

        # report best n values
        self.bestRarityResult()

    
    def bestRarityResult(self):

        argSortValues = np.argsort( self.rarityImg)
        sortValues = np.sort(self.rarityImg)

        printNBestValues = 100

        print("\nN best imgs:")
        print(argSortValues[:printNBestValues])

        print("\nN best values:")
        print(sortValues[:printNBestValues])