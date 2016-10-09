from collections import defaultdict
import operator
import re
import fileinput
from Canvas import Line
from _collections import defaultdict
from pandas.core.frame import DataFrame

class POSTag(object):
    
    # Construction initialization
    def __init__(self, trainingSetFile):
        self.trainingSetFile = trainingSetFile
        self.trainingSet = trainingSetFile.readlines()
        self.wordTagTable = {}
        self.wordProbTable = {}
        self.condnProbTable = {}
        self.newTagTable = {}
        self.errorTable = {}
        self.errorCountTable = {}
        self.topError = {}
        self.topErrorCount = {}
        self.topErrorDataFrame = DataFrame(columns=('Word','Tag','Error Probability'))
    
    #For conditional Probability Computation, given word and tag count Table    
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
    
    # Word count computation
    def computeWordProb(self, keyOne):
        self.wordProbTable[keyOne] = 0
        for keyTwo in self.wordTagTable[keyOne].keys():
            self.wordProbTable[keyOne] = self.wordProbTable[keyOne] + self.wordTagTable[keyOne][keyTwo]
    
    # Given a word , conditional probability of the tag computation
    def computeCondnProb(self):
        for keyOne in self.wordTagTable.keys():
            if keyOne not in self.condnProbTable.keys() :
                self.condnProbTable[keyOne] = {}
            self.computeWordProb(keyOne)
            for keyTwo in self.wordTagTable[keyOne].keys():
                self.condnProbTable[keyOne][keyTwo] = (float) (self.wordTagTable[keyOne][keyTwo])/self.wordProbTable[keyOne]
    
    #Most probable tag computation            
    def computeNewTags(self):
        for keyOne in self.wordTagTable.keys():
            self.newTagTable[keyOne] = max(self.condnProbTable[keyOne].iteritems(), key= operator.itemgetter(1))[0]
     
    #Writing a file with words and most probable tags                      
    def newTagFileWrite(self):
        newTagFile = open("newTagFile.txt", "a")
        for line in self.trainingSet:
            inputWithoutSpaces = line.split()
            for input in inputWithoutSpaces:
                inputValue = input.split("_")
                inputValue[1] = self.newTagTable[inputValue[0]]
                newTagFile.write(inputValue[0]+"_"+inputValue[1]+" ")
            newTagFile.write("\n")
     
    # Error analysis after the generation of words with most probable tags       
    def errorAnalysis(self):
        for keyOne in self.wordTagTable.keys():
            self.errorTable[keyOne] = {}
            countWord = 0
            for keyTwo in self.wordTagTable[keyOne].keys():
                countWord = countWord + self.wordTagTable[keyOne][keyTwo]
            mostProbableTag = self.newTagTable[keyOne]
            countWordTag = self.wordTagTable[keyOne][mostProbableTag]
            self.errorTable[keyOne] = (float)(countWord - countWordTag)/ countWord
            self.errorCountTable [keyOne] = countWord - countWordTag
     
    #Printing the top five erroneous word with most probable tags    
    def printTopErrors(self):
        self.topError = dict(sorted(self.errorTable.iteritems(), key = operator.itemgetter(1), reverse = True)[:5])
        self.topErrorCount = dict(sorted(self.errorCountTable.iteritems(), key = operator.itemgetter(1), reverse =True)[:5])
        count = 0
        print ("Error Analysis after assigning most Probable Tags")
        for value in sorted(self.topError.iteritems(), key = operator.itemgetter(1), reverse = True):
            #print(value)
            #keyOne = self.topError.keys()[self.topError.values().index(value)]
            self.topErrorDataFrame.loc[count] = [value[0], self.newTagTable[value[0]], value[1]]
            count = count + 1
        #for keyOne in self.topError.keys():
         #   topErrorDataFrame.loc[count] = [keyOne, self.newTagTable[keyOne], self.topError[keyOne]]
          #  count = count + 1
            #print (keyOne + " " + self.newTagTable[keyOne] + " " + str(self.topError[keyOne]))
        #print ("With Respect to Error Counts")
        #for keyOne in self.topErrorCount.keys():
        #    print (keyOne + " " + self.newTagTable[keyOne] + " " + str(self.topErrorCount[keyOne]))
        print (self.topErrorDataFrame)
    
    #Applying rules to the file
    def newRuleFileWrite(self):
        rule = {}
        replace = {}
        rule[1] = r'north_([A-Za-z]{2,4}) (?P<word>[A-Za-z]*)_NNP'
        replace[1] = r'north_JJ \g<word>_NNP'
        rule[2] = r'DT north_[A-Za-z]{2,4}'
        replace[2] = r'DT north_NN'
        rule[3] = r'_NN (?P<word1>[A-Za-z]*)_IN mid-January_[A-Za-z]{2,4} (?P<word>[A-Za-z]*)_IN'
        replace[3] = r'_NN \g<word1>_IN mid-January_JJ \g<word>_IN'
        rule[4] = r'(?P<word>[A-Za-z_ ]*)_NN cut_[A-Za-z]{2,4} '
        replace[4] = r'\g<word>_NN cut_VBD '
        rule[5] = r'cut_VB (?P<word>[A-Za-z _]*)VBD'
        replace[5] = r'cut_VBD \g<word>VBD'
        rule[6] = r'retired_[A-Za-z]{2,4} (?P<word>[A-Za-z]*)_NN(?P<word2>.*)'
        replace[6] = r'retired_JJ \g<word>_NN\g<word2>'
        rule[7] = r'(?P<word>[A-Za-z17]*)_-RRB- (?P<word2>[A-Za-z17:]*)_CD (?P<word3>[A-Za-z0-9:]*)_CD -0-_[A-Za-z]{2,4}'
        replace[7] = r'\g<word>_-RRB- \g<word2>_CD \g<word2>_CD -0-_.'
        
        newRuleFile = open("newTagFile.txt", "r")
        newFile =  open("newFinalFile.txt", "w")
        
        for line in newRuleFile.readlines():
            for count in xrange(1, 8):
                if(re.search(rule[count], line)):
                    line = re.sub(rule[count], replace[count], line)
            newFile.write(line)
    
    #Error Analysis after applying rules        
    def newError(self):
        myErrorTable = defaultdict(lambda: 0)
        finalFile = open("newFinalFile.txt", "r")
        lineCount = 0
        for lineTwo in finalFile.readlines():
            line = self.trainingSet[lineCount]
            lineCount = lineCount + 1
            tokenOne = line.split()
            tokenTwo = lineTwo.split()
            tokenCount = 0
            for inputTwo in tokenTwo:
                wordOne = tokenOne[tokenCount].split('_')
                tokenCount = tokenCount + 1
                wordTwo = inputTwo.split('_')
                if wordOne[0] == wordTwo[0] and wordOne[1] != wordTwo[1]:
                    myErrorTable[wordOne[0]] = myErrorTable[wordOne[0]] + 1
        myNewErrorDF = DataFrame(columns=['Word', 'New Error Probability'])    
        myErrorPercentage = {}
        count = 0 
        for keyOne in self.topErrorDataFrame.iloc[:,0]:
            countWord = 0
            for keyTwo in self.wordTagTable[keyOne].keys():
                countWord = countWord + self.wordTagTable[keyOne][keyTwo]
            myErrorPercentage[keyOne] = (float) (myErrorTable[keyOne])/countWord
            myNewErrorDF.loc[count]=[keyOne, myErrorPercentage[keyOne]]
            count = count + 1
        #print(myErrorPercentage)
        print("Error Analysis after applying rules")
        print(myNewErrorDF)
    
POSTagObject = POSTag(open("HW2_F16_NLP6320_POSTaggedTrainingSet-Unix.txt", "r"))
POSTagObject.computeCondnProbTable()
POSTagObject.computeCondnProb()
POSTagObject.computeNewTags()
POSTagObject.newTagFileWrite()
POSTagObject.errorAnalysis()
POSTagObject.printTopErrors()
POSTagObject.newRuleFileWrite()
POSTagObject.newError()


