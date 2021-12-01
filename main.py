import os
import cv2
import pdb
import matplotlib.pyplot as plt
import factoryImg as fImg


def main():

    # order is important
    layersName = ["baby", "claws", "bracelets", "eyes", "hair", "collars", "mouth", "skin", "face", "tails", "body", "wings",  "background"]
    itMustExists = [False, True, False, True, True, False, True, False, True, False, True, True, True]
    width = 798
    height = 860
    numberImgs = 100

    buildImg = fImg.factoryImg(".\layers", layersName, itMustExists, width, height)
    #buildImg.showAllImgs()

    img = buildImg.RandomImgs(numberImgs)


if __name__ == "__main__":

    main()