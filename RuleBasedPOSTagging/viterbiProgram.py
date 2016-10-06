import pandas as pd
import numpy as np
import operator
import sys

#Viterbi Class Implementation
class Viterbi:
    
    #Viterbi constructor
    def __init__(self, input):
        self.input = input
        numberList = list(xrange(1, len(input)+1))
        states = ["HOT","COLD","FINAL"]
        self.stringNumberList = [str(columnIndex) for columnIndex in numberList]
        self.pathProbMatrix = pd.DataFrame(index = states, columns = self.stringNumberList)
        #print([str(columnIndex) for columnIndex in numberList])
        self.backPointer = pd.DataFrame(index = states, columns = self.stringNumberList)
        self.tranisitionMatrix = self.initializeTransitionMatrix()
        self.stateObserMatrix = self.initializeStateObserMatrix()
    
    #Initialize the state transiton matrix
    def initializeTransitionMatrix(self):
        states = ["START","HOT","COLD", "FINAL"]
        data = [[0, 0.8, 0.2, 0],[0, 0.7, 0.3, 1],[0, 0.4, 0.6, 1]]
        transitionMatrix = pd.DataFrame(data, index=states[:-1], columns=states)
        print ("State Transition Matrix")
        print (transitionMatrix)
        return transitionMatrix
    
    #Initialize the state observation matrix
    def initializeStateObserMatrix(self):
        states = list(self.pathProbMatrix.index.values) 
        inputs = ["1","2","3"]
        data = [[0.2, 0.5],[0.4, 0.4],[0.4, 0.1]]
        stateObserMatrix = pd.DataFrame(data, index = inputs, columns = states[:-1])
        print ("State Observation Matrix")
        print (stateObserMatrix)
        return stateObserMatrix
    
    #To store all possible viterbi values of sequence encountered till previous step
    def maxStateList(self, states, timeStep, presentState, input):
        valList=[]
        for state in states[:-1]:
            valList.append(self.pathProbMatrix.loc[state, timeStep] * self.tranisitionMatrix.loc[state, presentState ] * self.stateObserMatrix.loc[input, presentState])
            
        return valList   
    
    #To store the values of possible backPointerValues 
    def maxBackPointerList(self, states, timeStep, presentState):
        backList=[]
        for state in states[:-1]:
            backList.append(self.pathProbMatrix.loc[state, timeStep] * self.tranisitionMatrix.loc[state, presentState ])
        #print backList    
        return backList           


    #viterbi algorithm implementation
    def viterbi(self):
        states=list(self.pathProbMatrix.index.values)
        #Initialization step
        for state in states[:-1]:
            #print(states)
            #print(state)
            #print(self.input[0])
            #print(self.tranisitionMatrix.loc["START", state])
            #print(self.stateObserMatrix.loc[self.input[0], state])
            self.pathProbMatrix.loc[state, "1"]= self.tranisitionMatrix.loc["START", state]*self.stateObserMatrix.loc[self.input[0], state]
            self.backPointer.loc[state, "1"] = "START";
        
        #Recursion step
        for timeStep in self.stringNumberList[1:]:
            for state in states[:-1]:
                valList = self.maxStateList(states, str(int(timeStep)-1), state, self.input[int(timeStep)-1])
                maxValue = max(valList)
                self.pathProbMatrix.loc[state, timeStep] = maxValue
                backList = self.maxBackPointerList(states, str(int(timeStep)-1), state)
                maxArg, maxValue = max(enumerate(backList), key=operator.itemgetter(1))
                #print ("maxArg " + str(maxArg) + " value " + states[maxArg])
                #print ("timeStep" + timeStep)
                self.backPointer.loc[state, timeStep] = states[maxArg]
                #print (state +" "+ timeStep)
        #Termination step
        backList = self.maxBackPointerList(states, str(len(self.input)) , "FINAL")
        maxArg, maxValue = max(enumerate(backList), key=operator.itemgetter(1))
        #print ("maxArg " + str(maxArg) + " value " + states[maxArg])
        self.pathProbMatrix.loc["FINAL", str(len(self.input))] = maxValue
        self.backPointer.loc["FINAL", timeStep] = states[maxArg]
        
    #Traceback for printing the eather sequence 
    def printBackPointer(self):
        printBackPointer = [self.backPointer.loc["FINAL", str(len(self.input))]]
        currentPosition = len(self.input)
        while(currentPosition!=1):
            printBackPointer.insert(0, self.backPointer.loc[printBackPointer[0], str(currentPosition)])
            currentPosition=currentPosition-1
        print(printBackPointer)
            
        
#Getting the command line arguments as inputs
for input in sys.argv[1:]:
    print("Input Sequence is " + input)
    myViterbi = Viterbi(input)     
    myViterbi.viterbi()
    print("Path Probabiltiy Matrix")
    print(myViterbi.pathProbMatrix) 
    print("Back Pointer Matrix")
    print(myViterbi.backPointer) 
    print("The most likely weather sequence for " + input +" is as follows")
    myViterbi.printBackPointer()             
                

  