from __future__ import print_function
from __future__ import division
from collections import defaultdict
import pandas
 
def printValues(stringword, dict, defaultValue):
    for index in stringword:
        for value in stringword:
            if index not in biGram.keys() and defaultValue == 0:
                biGram[index][value] = 0
            if value not in biGram[index].keys() and defaultValue == 0:
                biGram[index][value] = 0
    pandas.set_option('display.width', 10000)
    pandas.set_option('precision', 15)
    di=pandas.DataFrame(dict, stringword, stringword)
    di.round(decimals=10)
    print (di.transpose().fillna(value=defaultValue))
    return dict        
def computeUniGram(corpus):
    tokens = corpus.split()
    unigram=defaultdict(lambda: 0)
    for index in tokens:
        unigram[index]=unigram[index]+1
    return unigram

def computeBiGram(corpus, defaultValue):
    tokens = corpus.split()
    biGram = defaultdict(dict)
    for index in xrange(0, len(tokens)):
        biGram[tokens[index]]=defaultdict(lambda: defaultValue)
    for index in xrange(0, len(tokens)-1):
        biGram[tokens[index]][tokens[index+1]]=biGram[tokens[index]][tokens[index+1]]+1
    return biGram

def computeDefaultProb(unigram, biGram, myString):
    tokens=myString.split()
    defaultProb={}
    for tokenOne in tokens:
        defaultProb[tokenOne] = defaultdict(lambda: 0.0)
        for tokenTwo in tokens:
            countOne=unigram[tokenOne]
            countOneTwo=biGram[tokenOne][tokenTwo]
            if countOne != 0.0:
                defaultProb[tokenOne][tokenTwo]=countOneTwo/countOne
            else:
                defaultProb[tokenOne][tokenTwo]=0.0
    return defaultProb
    
def computeOneSmoothProb(unigram, biGram, myString):
    tokens=myString.split()
    defaultProb={}
    for tokenOne in tokens:
        defaultProb[tokenOne] = defaultdict(lambda: 0.0)
        for tokenTwo in tokens:
            countOne=unigram[tokenOne] + uniqueTokenLength
            countOneTwo=biGram[tokenOne][tokenTwo] 
            if countOne != 0.0:
                defaultProb[tokenOne][tokenTwo]=countOneTwo/countOne
            else:
                defaultProb[tokenOne][tokenTwo]=0.0
    return defaultProb
    
def computeString(s, biGramCorpus, defaultValue):
    tokens = s.split()
    biGram = {}
    for tokenOne in tokens:
        biGram[tokenOne] = defaultdict(lambda: defaultValue)
    	for tokenTwo in tokens:
		if tokenOne in biGramCorpus and tokenTwo in biGramCorpus[tokenOne]:
            	    biGram[tokenOne][tokenTwo] = biGramCorpus[tokenOne][tokenTwo]
    biGram = printValues(tokens, biGram, defaultValue)
    return biGram

def computeGoodTuringBiGram(corpusString, biGram):
    countValue = defaultdict(lambda: 0)
    for tokenOne in corpusString:
        for tokenTwo in corpusString:
            count = biGram[tokenOne][tokenTwo]
            countValue[count] = countValue[count]+1
    return countValue         
            
def computeCStar(goodbiGram):
    cStarGram = defaultdict(lambda: 0)
    for keys in goodbiGram.keys():
        if goodbiGram[keys+1] == 0:
            cStarGram[keys] = 0
        elif goodbiGram[keys] == 0:
            cStarGram[keys] = 0
        else:
            cStarGram[keys]=(keys+1)*(goodbiGram[keys+1])/(goodbiGram[keys])
    return cStarGram   

def printGoodTuringTable(myString, goodBiGram, cStarGram):
    for keys in goodBiGram.keys():
        print(str(keys) + " " + str(cStarGram[keys]) + " " + str(goodBiGram[keys]))

def printGoodTuring(myString, biGram, goodBiGram, cStarGram, goodProbTable):
    setOne=set()
    for index in xrange(0, (len(myString)-1)):
        keys = biGram[myString[index]][myString[index+1]]
        setOne.add(keys)
    setOne=sorted(setOne)
    print("c" , end="")
    df=pandas.DataFrame(columns=("c* Value","NcValue", "P* Value"))
    for keys in setOne:
        df.loc[keys] = [cStarGram[keys], goodBiGram[keys], goodProbTable[keys]]
    print(df)
        
def calculateProb(myString, biGramProb, uniGram, corpusLength):
    prob = uniGram[myString[0]]/(corpusLength)
    for index in xrange(1,  (len(myString))):
        prob = prob * biGramProb[myString[index-1]][myString[index]]
    print (prob)

def calculateGoodProb(corpusLength, goodBiGram, cStarGram):
    goodProbTab = {}
    goodProbTab[0] = goodBiGram[1]/corpusLength
    for c in cStarGram.keys():
       if c != 0:
           goodProbTab[c] = cStarGram[c]/corpusLength
    return goodProbTab

def calculateGoodFinalProb(myString, biGram, goodProbTab, uniGram, corpusLength):
    prob = uniGram[myString[0]]/(corpusLength)
    for index in xrange(1, (len(myString))):
        prob = prob * goodProbTab[biGram[myString[index-1]][myString[index]]]
    print (prob)

    
 
global biGram, biGramOne, uniqueTokenLength
corpus = open('NLPCorpusTreebank2Parts-CorpusA-Unix.txt')
corpusString=corpus.read().upper()
uniqueTokenLength = len(set(corpusString.split()))
s1 = "The president has relinquished his control of the company's board."
s2 = "The chief executive officer said the last year revenue was good."
s1 = s1.upper()
s2 = s2.upper()
uniGram = computeUniGram(corpusString)
biGram = computeBiGram(corpusString, 0)


print("\nBigram Model without Smoothing for the Sentence S1\n")
print("\nB. 1) Table with the BiGram Counts\n")
biGramTokenOne = computeString(s1, biGram, 0)
defaultProbOne = computeDefaultProb(uniGram, biGramTokenOne, s1)
print ("\nB. 2) Table with the BiGram Probability\n")
defaultProbOne = printValues(s1.split(), defaultProbOne, 0)
print ("\nB. 3) Total Probability of the Sentence S1")
calculateProb(s1.split(), defaultProbOne, uniGram, len(corpusString.split()))

print("\nBigram Model with add-one Smoothing for the Sentence S1\n")
print("\nC. 1) Table with the BiGram Counts\n")
biGramOne = computeBiGram(corpusString, 1)
biGramTokenOneSmooth = computeString(s1, biGramOne, 1)
print ("\nC. 2) Table with the BiGram Probability\n")
smoothProbOne = computeOneSmoothProb(uniGram, biGramTokenOneSmooth, s1)
smoothProbOne = printValues(s1.split(), smoothProbOne, 1)
print ("\nC. 3) Total Probability of the Sentence S1")
calculateProb(s1.split(), smoothProbOne, uniGram, len(corpusString.split()))


print("\nBigram Model Good Turing Discounting for the Sentence S1\n")
goodBiGram = computeGoodTuringBiGram(set(corpusString.split()), biGram)
cStarGram = computeCStar(goodBiGram)
goodProbTable = calculateGoodProb(len(corpusString.split()), goodBiGram, cStarGram)
print("\nD. 1) and 2) Table with the BiGram Counts and Probability\n")
printGoodTuring(s1.split(), biGram, goodBiGram, cStarGram, goodProbTable)
print ("\nD. 3) Total Probability of the Sentence S1")
calculateGoodFinalProb(s1.split(), biGram, goodProbTable, uniGram, len(corpusString.split()))


print("\nBigram Model without Smoothing for the Sentence S2\n")
print("\nB. 1) Table with the BiGram Counts\n")
biGramTokenTwo = computeString(s2, biGram, 0)
defaultProbTwo = computeDefaultProb(uniGram, biGramTokenTwo, s2)
print ("\nB. 2) Table with the BiGram Probability\n")
defaultProbTwo = printValues(s2.split(), defaultProbTwo, 0)
print ("\nB. 3) Total Probability of the Sentence S2")
calculateProb(s2.split(), defaultProbTwo, uniGram, len(corpusString.split()))


print("\nBigram Model with add-one Smoothing for the Sentence S2\n")
print("\nC. 1) Table with the BiGram Counts\n")
biGramTokenTwoSmooth = computeString(s2, biGramOne, 1)
smoothProbTwo = computeOneSmoothProb(uniGram, biGramTokenTwoSmooth, s2)
print ("\nC. 2) Table with the BiGram Probability\n")
smoothProbTwo = printValues(s2.split(), smoothProbTwo, 1)
print ("\nC. 3) Total Probability of the Sentence S2")
calculateProb(s2.split(), smoothProbTwo, uniGram, len(corpusString.split()))

print("\nBigram Model Good Turing Discounting for the Sentence S2\n")
print("\nD. 1) and 2) Table with the BiGram Counts and Probability\n")
printGoodTuring(s2.split(), biGram, goodBiGram, cStarGram, goodProbTable)
print ("\nD. 3) Total Probability of the Sentence S2")
calculateGoodFinalProb(s2.split(), biGram, goodProbTable, uniGram, len(corpusString.split()))

corpus.close()