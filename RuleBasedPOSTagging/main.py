from collections import defaultdict
import operator

class POSTag(object):
    
    def __init__(self, trainingSetFile):
        self.trainingSetFile = trainingSetFile
        self.trainingSet = trainingSetFile.readlines()
        self.wordTagTable = {}
        self.wordProbTable = {}
        self.condnProbTable = {}
        self.newTagTable = {}
        
    def computeCondnProbTable(self):
        for line in self.trainingSet:
            inputWithoutSpaces = line.split()
            for input in inputWithoutSpaces:
                inputValue = input.split("_")
                if inputValue[0] not in self.wordTagTable.keys() :
                    self.wordTagTable[inputValue[0]] = {}
                    self.wordTagTable[inputValue[0]][inputValue[1]] = 1
                elif inputValue[1] not in self.wordTagTable[inputValue[0]].keys() :
                    self.wordTagTable[inputValue[0]][inputValue[1]] = 1
                else:
                    self.wordTagTable[inputValue[0]][inputValue[1]] = self.wordTagTable[inputValue[0]][inputValue[1]] + 1    
    
    def computeWordProb(self, keyOne):
        self.wordProbTable[keyOne] = 0
        for keyTwo in self.wordTagTable[keyOne].keys():
            self.wordProbTable[keyOne] = self.wordProbTable[keyOne] + self.wordTagTable[keyOne][keyTwo]
    
    def computeCondnProb(self):
        for keyOne in self.wordTagTable.keys():
            if keyOne not in self.condnProbTable.keys() :
                self.condnProbTable[keyOne] = {}
            self.computeWordProb(keyOne)
            for keyTwo in self.wordTagTable[keyOne].keys():
                self.condnProbTable[keyOne][keyTwo] = self.wordTagTable[keyOne][keyTwo]/self.wordProbTable[keyOne]
                
                
    def computeNewTags(self):
        for keyOne in self.wordTagTable.keys():
            self.newTagTable[keyOne] = max(self.condnProbTable[keyOne], key= lambda i: self.condnProbTable[keyOne][i])
                           
    def newTagFileWrite(self):
        newTagFile = open("newTagFile.txt", "a")
        for line in self.trainingSet:
            inputWithoutSpaces = line.split()
            for input in inputWithoutSpaces:
                inputValue = input.split("_")
                inputValue[1] = self.newTagTable[inputValue[0]]
                newTagFile.write(inputValue[0]+"_"+inputValue[1]+" ")
                print (inputValue[0]+"_"+inputValue[1]+" ")
            newTagFile.write("\n")
                
        
        
    
trainingSetFile = open("HW2_F16_NLP6320_POSTaggedTrainingSet-Unix.txt", "r")
print trainingSetFile.readline()
POSTagObject = POSTag(open("HW2_F16_NLP6320_POSTaggedTrainingSet-Unix.txt", "r"))
POSTagObject.computeCondnProbTable()
POSTagObject.computeCondnProb()
POSTagObject.computeNewTags()
POSTagObject.newTagFileWrite()
