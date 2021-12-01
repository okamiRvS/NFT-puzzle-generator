import os
import cv2
import pdb
from PIL import Image
import matplotlib.pyplot as plt
import factoryImg as fImg


def main():

    # order is important
    layersName = ["baby",
                  "claws",
                  "bracelets", 
                  "eyes", 
                  "hair", 
                  "collars", 
                  "mouth", 
                  "face", 
                  "tails", 
                  "body", 
                  "wings", 
                  "background"]
    numberImgs = 100

    buildImg = fImg.factoryImg(".\layers", layersName)
    #buildImg.showAllImgs()

    img = buildImg.RandomImgs(numberImgs)


if __name__ == "__main__":

    main()