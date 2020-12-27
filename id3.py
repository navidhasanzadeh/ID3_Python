# By Navid Hasanzadeh 9323701
"""
Created on Fri Mar 23 14:04:43 2018

@author: Navid Hasanzadeh
"""
import pandas as pd
import numpy as np
from branch import branch
from leaf import leaf
from copy import deepcopy

class id3:
    def __init__(self, file=None):
        self.__file = file
        self.__lineNumber = 0
        self.__predictData = None
        self.__pruneData = None
        self.__featuresValues = None
        self.__learnedNode = None
        self.__test = None
        self.__goalColumn = None
        self.__nodesNumber = 0
        self.__leavesNumber = 0
        self.__nodeDic = {}
        self.__removedNodesNumber = []      
        self.__seenNodes=[]
        self.__pruneTestErrors = []
    def retNodeDic(self):
        self.__learnedNode.makeNodeList(self.__learnedNode, self.__nodeDic)
        return self.__nodeDic
    def __clean(self):        
        self.__lineNumber = 0
        self.__predictData = None
        self.__featuresValues = None        
    def __entropy(self, series):
        S = 0
        length = series.nunique()
        a = series.value_counts()
        for j in range(0, length):
            p = a[j] / series.size
            S = S + -1 * p * np.log2(p)
        return S
    def __gain(self, series):
        length = series[series.columns[1]].nunique()
        a = series[series.columns[1]].value_counts()
        S0 = self.__entropy(series[series.columns[0]])
        g = S0
        for i in range(0, length):
            series2 = series[series[series.columns[1]]==a.index[i]]
            p = a[i] / (series.size/2)
            g = g - p * self.__entropy(series2[series2.columns[0]])
        return g

    def __selectDf(self, df1, featureIndex, value):
        df = deepcopy(df1)
        newdf = df[df[df.columns[featureIndex]]==value]
        newdf = newdf.drop(newdf.columns[featureIndex], axis=1)
        newdf = newdf.reset_index(drop=True)
        return newdf
    def __findDFMaxGainFeature (self, df,goalColumnNum):
        maxG = 0
        maxGIndex = 0
        for i in range(0,df.columns.size):
            if(i != goalColumnNum):
                g = self.__gain(df[df.columns[[int(goalColumnNum),i]]])
                if g>=maxG:
                    maxG = g                    
                    maxGIndex = i
        return [maxGIndex, maxG]
    def __getFeatureValues(self, featuresValues, featureName):
        values = featuresValues[featureName].tolist()[0]
        return values
    def __vote(self, df, goalColumnNum):
        goalColumnValues = self.__featuresValues[list(self.__featuresValues.columns.values)[goalColumnNum]][0]
        valuesNumbers = pd.Series(np.array([0] * len(goalColumnValues)) ,index=goalColumnValues)
        length = len(df[df.columns[int(goalColumnNum)]])
        valuesNumbers = (valuesNumbers + df[df.columns[int(goalColumnNum)]].value_counts()).fillna(0)
        maxValue = max(valuesNumbers.values)
        maxValueIndex = int(valuesNumbers.index[valuesNumbers==maxValue].values[0])
        return [maxValue/length,valuesNumbers ,valuesNumbers.index[valuesNumbers.index==str(maxValueIndex)].tolist()]
    def __grow(self, df, goalColumnNum): 
        self.__nodesNumber += 1 
        print('-', end='')
        [voteP, valuesCount, voteValue] = self.__vote(df, goalColumnNum)
        if(voteP == 1 or len(df.columns)==1 or voteP == 0):
            newLeaf = leaf(voteValue)
            newLeaf.setValuesCount(valuesCount)
            self.__leavesNumber += 1
            return newLeaf
        else:
            [maxGIndex, maxG] = self.__findDFMaxGainFeature(df, goalColumnNum)
            node = branch(df.columns[maxGIndex], self.__getFeatureValues(self.__featuresValues, df.columns[maxGIndex]), maxG)
            featureValues = self.__getFeatureValues(self.__featuresValues,df.columns[maxGIndex])
            print(df.columns[maxGIndex])
            for value in featureValues:
                nextDF = self.__selectDf(df, maxGIndex, value)
                if(len(nextDF[nextDF.columns[goalColumnNum]])==0):
                    newLeaf = leaf(voteValue)
                    self.__leavesNumber += 1
                    newLeaf.setValuesCount(valuesCount)
                    node.setNext(value, newLeaf)        
                else:
                    nextNode = self.__grow(nextDF, goalColumnNum)                 
                    node.setNext(value, nextNode)        
            return node
    def learn(self, file=None):        
        if(file!=None):
            self.__file = file
        with open(self.__file) as fp:
            for line in fp:
                self.__lineNumber = self.__lineNumber + 1
                rowWords = line.split()
                if(self.__lineNumber == 1):
                    goalColumnNum = int(rowWords[1])                    
                if(self.__lineNumber == 2):
                    self.__predictData = pd.DataFrame(columns = rowWords)        
                if(self.__lineNumber > 3):
                    self.__predictData.loc[self.__lineNumber-4] = rowWords
            self.__featuresValues = pd.DataFrame(columns = list(self.__predictData.columns.values))
            for i in range(0,len(self.__predictData.columns)):
                self.__featuresValues[list(self.__predictData.columns.values)[i]] = [list(self.__predictData[self.__predictData.columns[i]].value_counts().index)]
        self.__nodesNumber = 0        
        self.__leavesNumber = 0
        res = self.__grow(self.__predictData, goalColumnNum)
        self.__learnedNode = res
        self.retNodeDic()
        self.__clean()
        return res

    def getNodesNumber(self):
        return self.__nodesNumber
    def getLeavesNumber(self):
        return self.__leavesNumber
    def getTreeSize(self):
        return self.__leavesNumber + self.__nodesNumber
    def __predict(self, inputdf, goalColumnNum, node=None, idN=0):
        df = deepcopy(inputdf)
        nodeI = node             
        result = []
        for i in range(0, len(df)):
            selectedRow = df.loc[i]
            if(nodeI is None):
                node = self.__learnedNode
            else:
                node = nodeI
            while (node.isLeaf == False):
                node = node.getNext(selectedRow[node.getFeature()])
            result.append(node.getValue()[0])
            if(idN != 0):
                if(id(node)==idN):
                    print('BALI')
        df['predict'] = result            
        return df

    def treePrune(self, file, node=None, testFile = None, trainFile = None):
        if(node!=None):
            self.__learnedNode = node
        if(testFile!=None and trainFile!=None):
            self.__pruneTestErrors=[]
            trainErr = self.getError(self.predict(trainFile))
            self.__pruneTestErrors.append(trainErr)
            testErr = self.getError(self.predict(testFile))            
            self.__pruneTestErrors.append(testErr)
            validErr = self.getError(self.predict(file))
            self.__pruneTestErrors.append(validErr)            
        with open(file) as fp:
            for line in fp:
                self.__lineNumber = self.__lineNumber + 1
                rowWords = line.split()
                if(self.__lineNumber == 1):
                    # attributeNum = rowWords[0]
                    goalColumnNum = int(rowWords[1])
                if(self.__lineNumber == 2):
                    # attributeList = rowWords
                    self.__pruneData = pd.DataFrame(columns = rowWords)        
                if(self.__lineNumber > 3):
                    self.__pruneData.loc[self.__lineNumber-4] = rowWords
            self.__featuresValues = pd.DataFrame(columns = list(self.__pruneData.columns.values))
            for i in range(0,len(self.__pruneData.columns)):
                self.__featuresValues[list(self.__pruneData.columns.values)[i]] = [list(self.__pruneData[self.__pruneData.columns[i]].value_counts().index)]
        self.retNodeDic()
        self.__goalColumn = self.__pruneData.columns[goalColumnNum]        
        self.__learnedNode = (self.__prune(self.__pruneData, goalColumnNum, self.__learnedNode, testFile, trainFile))
        self.__clean() 
        return self.__learnedNode
    def pruneTestErrors(self):
        return self.__pruneTestErrors
    def __prune(self, df, goalColumnNum, node, testFile, trainFile):
        lN = self.__learnedNode        
        pNode = 0
        tempLeaf = 0    
#        import pdb; pdb.set_trace()
        self.__removedNodesNumber = []
        for i in range(len(self.__nodeDic),1,-1):
            print('level:', i)
            for pNode in self.__nodeDic[i]:        
                if(not(id(pNode) in self.__seenNodes)):
                    self.__seenNodes.append(id(pNode))
                    predict1 = self.__predict(df, goalColumnNum, node = lN)
                    error1 = self.getError(predict1)
                    tempLeaf = leaf(pNode.getMostValue())
                    tempLeaf.setValuesCount(pNode.getValuesCount())
                    backupNode = pNode
                    prevNode = pNode.getPreviousNode()
                    prevNode.jRemoveNext(pNode.getPrevValue())
                    prevNode.jSetNext(pNode.getPrevValue(), tempLeaf)                
                    predict2 = self.__predict(df, goalColumnNum, node = lN)
                    error2 = self.getError(predict2)
                    if(error2 > 0.995 * error1):
                        prevNode.jRemoveNext(pNode.getPrevValue())
                        prevNode.jSetNext(pNode.getPrevValue(), backupNode)                    
                        predict3 = self.__predict(df, goalColumnNum, node = lN)
                        dic = {}
                        error3 = self.getError(predict3)
                        self.__nodeDic = self.retNodeDic()
                    else:                    
                        prevNode.jRemoveNext(pNode.getPrevValue())
                        prevNode.jSetNext(pNode.getPrevValue(), tempLeaf)
                        del(pNode)
                        self.__removedNodesNumber.append(error2)
                        dic = {}
                        self.__nodeDic = self.retNodeDic()
                        if(testFile!=None and trainFile!=None):
                            testErr = self.getError(self.predict(testFile))
                            trainErr = self.getError(self.predict(trainFile))
                            self.__pruneTestErrors.append(trainErr)
                            self.__pruneTestErrors.append(testErr)
                            self.__pruneTestErrors.append(error2)
        return self.__learnedNode 
    def predict(self, file, node=None):
        if(node!=None):
            self.__learnedNode = node      
        self.__lineNumber = 0
        with open(file) as fp:
            for line in fp:
                self.__lineNumber = self.__lineNumber + 1
                rowWords = line.split()
                if(self.__lineNumber == 1):
                    goalColumnNum = int(rowWords[1])
                if(self.__lineNumber == 2):
                    self.__predictData = pd.DataFrame(columns = rowWords)        
                if(self.__lineNumber > 3):
                    self.__predictData.loc[self.__lineNumber-4] = rowWords
            self.__featuresValues = pd.DataFrame(columns = list(self.__predictData.columns.values))
            for i in range(0,len(self.__predictData.columns)):
                self.__featuresValues[list(self.__predictData.columns.values)[i]] = [list(self.__predictData[self.__predictData.columns[i]].value_counts().index)]
        self.__goalColumn = self.__predictData.columns[goalColumnNum]        
        df = self.__predict(self.__predictData, goalColumnNum)
        self.__clean() 
        return df
    def getError(self, df):
        column1name = self.__goalColumn
        column2name = 'predict'
        result =[]
        for i in range(0, len(df)):
            selectedValue1 = int(df[column1name].loc[i])            
            selectedValue2 = int(df[column2name].loc[i])
            result.append(abs(selectedValue2-selectedValue1))
        err = np.mean(result)
        return err