# By Navid Hasanzadeh 9323701
"""
Created on Sat Mar 24 14:57:04 2018

@author: Navid
"""
class leaf:
    def __init__(self, value):
        self.value = value
        self.valuesCount = None
        self.isLeaf = True
        self.root = self
        self.previousNode = None
        self.prevValue = None
        self.gain = 0
    def setGain(self, gain):
        self.gain = gain
    def getGain(self):
        return self.gain
    def getPrevValue(self):
        return self.prevValue
    def setPrevValue(self, value):
        self.prevValue = value 
    def getValue(self):
        return self.value[0]
    def setPreviousNode(self, node):
        self.previousNode = node
    def getPreviousNode(self):
        return self.previousNode
    def setValuesCount(self,valuesCount):
        self.valuesCount = valuesCount
    def getValuesCount(self):
        return self.valuesCount
    def setValue(self, value):
        self.value = value
    def printBranch(self,space=0, fake=False, until=0):
        print(self.value)
    def setRoot(self, node):
        self.root = node
    def getRoot(self):
        return self.root
        