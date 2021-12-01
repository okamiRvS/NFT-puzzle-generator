import os
import cv2
import pdb
import matplotlib.pyplot as plt


class puzzle():
   
    def __init__(self) -> None:

        puzzleImgs = []
        for root, dirs, files in os.walk(".\puzzle", topdown=True):
            for file in files:
                pathImg = os.path.join(root, file)
                puz = cv2.imread(pathImg, cv2.IMREAD_UNCHANGED)
                puzzleImgs.append(puz)
        
        self.puzzleImgs = puzzleImgs
        
    def puzzling(self, img):
        dst = []
        for puz in self.puzzleImgs:

            dst.append(cv2.bitwise_and(puz, img))

        return dst


    def show(self, img, time):

        fig = plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGBA))
        plt.axis('off')
        fig.axes.get_xaxis().set_visible(False)
        fig.axes.get_yaxis().set_visible(False)
        plt.pause(time)
        plt.clf()


def main():
    
    tmp = puzzle()

    for puz in tmp.puzzleImgs:

        tmp.show(puz, 1)

if __name__ == "__main__":

    main()