# By Navid Hasanzadeh 9323701
"""
Created on Sat Mar 24 14:56:53 2018

@author: Navid
"""
import math
#import pydot
#import os
#os.environ["PATH"] += os.pathsep + 'C:/Program Files (x86)/Graphviz2.38/bin/'
class branch:
    def __init__(self, feature, featureValues, gain=0):
        self.feature = feature
        self.featureValues = featureValues
        self.next = [None] * len(self.featureValues)
        self.hasNext = False
        self.isLeaf = False
        self.valuesCount = None
        self.root = self
        self.previousNode = self
        self.prevValue = None
        self.gain = gain
        self.index = 1
        self.nodeList= {}
    def getNodeLevelList(self):
        return self.getRoot().nodeList
    def setGain(self, gain):
        self.gain = gain
    def setIndex(self, index):
        self.index = index
    def getIndex(self):
        return self.index
    def getGain(self):
        return self.gain
# Decision Tree Graph Export by Pydot    
#    def exportGraph(self, exportFile='graph.png'):        
#        graph = pydot.Dot(graph_type="graph")
#        self.__addGraphNode(graph, self) 
#        graph.write_png(exportFile)
#    def __addGraphNode(self, graph, node):      
##        import pdb; pdb.set_trace()
#        if(node.isLeaf == False):
#            label = node.getValue() + '\n'+ str(node.getGain())  + '\n'+ str(id(node))
#            gnode = pydot.Node(label, style="filled", fillcolor="orange")        
#        else:
#            label = node.getValue()  + '\n'+ str(id(node.getPreviousNode()))
#            gnode = pydot.Node(label, style="filled", fillcolor="green")
#        graph.add_node(gnode)
#        if(node.isLeaf == False):
#            for value in node.getFeatureValues():
#                self.__addGraphNode(graph, node.getNext(value))
#                if(node.getNext(value).isLeaf):
#                    label2 = node.getNext(value).getValue() + '\n'+ str(id(node))
#                else:
#                    label2 = node.getNext(value).getValue() + '\n'+ str(node.getNext(value).getGain()) + '\n'+ str(id(node.getNext(value)))
#                graph.add_edge(pydot.Edge((label, (label2)),label=value))
    def makeNodeList(self, node, dic):
        if(node.isLeaf== False):
            if node.index in dic:
                (dic[node.index]).append(node)
            else:
                dic[node.index] = [node]
            for value in node.getFeatureValues():
                index = node.index + 1
                if(node.getNext(value).isLeaf == False):
                    node.getNext(value).setIndex(index)
                    self.makeNodeList(node.getNext(value), dic)

    def setRoot(self, node):
        self.root = node
    def getRoot(self):
        return self.root
    def setPreviousNode(self, node):
        self.previousNode = node
    def getValue(self):
        return self.feature
    def getPreviousNode(self):
        return self.previousNode
    def getFeature(self):
        return self.feature
    def getFeatureValues(self):
        return self.featureValues
    def setValuesCount(self,valuesCount):
        self.valuesCount = valuesCount
    def getValuesCount(self):
        return self.valuesCount
    def getPrevValue(self):
        return self.prevValue
    def setPrevValue(self, value):
        self.prevValue = value        
    def removeNext(self, featureValue, dic = None):
        self.valuesCount = self.valuesCount - self.getNext(featureValue).getValuesCount()
        if(dic != None and self.getNext(featureValue).isLeaf == False):
            list(dic[self.getNext(featureValue).getIndex()]).remove(self.getNext(featureValue))
            if len(list(dic[self.getNext(featureValue).getIndex()]))==0:
                del(dic[self.getNext(featureValue).getIndex()])
        self.next[self.featureValues.index(featureValue)] = None    
    def addValuesCount(self,valuesCount):
        if (self.valuesCount is None):
            self.valuesCount = valuesCount
        else:
            self.valuesCount = valuesCount + self.valuesCount
    def getNext(self, value):
        return self.next[self.featureValues.index(value)]
    def getMostValue(self):
        return self.valuesCount.index[self.valuesCount==max(self.valuesCount)].tolist()[0]
    def setNext(self, featureValue, newNext):        
        self.hasNext = True
        self.addValuesCount(newNext.getValuesCount())
        self.next[self.featureValues.index(featureValue)] = newNext
        newNext.setPreviousNode(self)
        newNext.setRoot(self.root)
        newNext.setPrevValue(featureValue)
    def jSetNext(self, featureValue, newNext):
        self.next[self.featureValues.index(featureValue)] = newNext
    def jRemoveNext(self, featureValue, dic = None):
        self.next[self.featureValues.index(featureValue)] = None
    def getMaxLevel(self):
        return max(list(self.nodeList.keys()))
    def printBranch(self, space=0, until=0):          
          for i in range(0, len(self.featureValues)):              
            print(self.feature,':',self.featureValues[i],'>> ', end='')
            if(self.hasNext):
                self.next[self.featureValues.index(self.featureValues[i])].printBranch(len(self.feature) + len(self.featureValues[i]) + 7 + space)
            
            if(i< len(self.featureValues) -1):
                print(' ' * (space),end='')