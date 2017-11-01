import os
import re
import csv

class GrammarParser:

    def __init__(self,rulesFile,sentenceFile):
        self.rulesFile=rulesFile
        self.sentenceFile=sentenceFile
        self.rules=[]
        self.sentences=[]
        self.nonTerminals=set()

    def parseRulesFile(self):
        with open(self.rulesFile, "r") as ins:
            array = []
            for line in ins.readlines():
                splits=line.split("\r")
                for i in range(0,len(splits)):
                    splits2=splits[i].split(" ")
                    self.rules.append(splits2)
                    for j in range(0,len(splits2)-1):
                        if splits2[j].isupper():
                            self.nonTerminals.add(splits2[j])

        print "\nRules are updated after parsing the file \n",self.rules
        print "\nNon-Terminals also updated\n",self.nonTerminals
        return self.rules;



    def parseSentsFile(self):
        with open(self.sentenceFile, "r") as ins:
            array = []
            for line in ins.readlines():
                splits=line.split("\n")
                for i in range(0,len(splits)):
                    splits2=splits[i].split(" ")
                    if splits2!=None and len(splits2)!=0 and len(splits2[0])>0:
                        self.sentences.append(splits2)


        print "Sentences are updated after parsing the file \n",self.sentences

        return self.sentences