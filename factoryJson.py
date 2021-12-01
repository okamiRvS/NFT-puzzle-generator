import os
import cv2
import pdb
import puzzle as puzz
import json
import hashlib
import datetime
import copy


class factoryJson():

    def __init__(self) -> None:

        self.jsonFile = []


    def createMetaDataJson(self, imgFolder):

        # convert into JSON:
        y = json.dumps(self.jsonFile, indent=4)

        # the result is a JSON string:        
        #print(y)

        # save
        with open(f'{imgFolder}/_metadata.json', 'w') as file:
            json.dump(self.jsonFile, file, indent=4)


    def createSingleJson(self, imgFolder, ofThisImg):

        # save
        with open(f'{imgFolder}/{ofThisImg}.json', 'w') as file:
            json.dump(self.jsonFile[ofThisImg], file, indent=4)


    def createPuzzleJson(self, imgFolder, ofThisImg):

        data = copy.deepcopy(self.jsonFile[ofThisImg])

        # save
        for i in range(9):
            with open(f'{imgFolder}/{ofThisImg}/{i}.json', 'w') as file:
                data["puzzle"] = i
                json.dump(data, file, indent=4)


    def buildJson(self, randDecision, attributes, currentImg):

        hash = hashlib.md5(json.dumps(randDecision).encode('utf-8')).hexdigest()

        '''
        # SAVE A
        # Driver code  
        data = {
            "hash": hash,
            "decodedHash": randDecision,
            "edition": currentImg,
            "date": datetime.datetime.now().timestamp(),
            "attributes": attributes
        }
        '''

        data = {
            "dna": hash,
            "name": f"#{currentImg}",
            "description": "This is the description of your NFT project",
            "image": f"https://hashlips/nft/{currentImg}.png",
            "edition": currentImg,
            "date": datetime.datetime.now().timestamp(),
            "attributes": attributes,
            "compiler": "HashLips Art Engine"
        }

        self.jsonFile.append(data)

        return data