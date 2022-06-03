import os
import cv2
import pdb
import matplotlib.pyplot as plt
import factoryImg as fImg


def main():

    # order is important
    layersData = {
        # "nameLayer": [itMustExists?, [LayerForeground, AfterLayer] 
        "baby": [False],
        "claws": [True],
        "mouth": [True],
        "special": [False, ["special-foreground", "wings"]],
        "eyes": [True],
        "ears": [False],
        "hair": [True],
        "bracelets": [False],
        "collars": [False],
        "tails": [False],
        "tattoo": [False],
        "skin": [False],
        "face": [True],
        "body": [True],
        "wings": [True],
        "aura": [False],
        "background": [True]
    }

    width = 798
    height = 860
    numberImgs = 5000

    buildImg = fImg.factoryImg(".\layers", layersData, width, height, numberImgs)
    #buildImg.showAllImgs()

    img = buildImg.RandomImgs(numberImgs)


if __name__ == "__main__":

    main()