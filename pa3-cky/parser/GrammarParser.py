import os
import re
import csv

class GrammarParser:

    def __init__(self,rulesFile,sentenceFile):
        self.rulesFile=rulesFile
        self.sentenceFile=sentenceFile
        self.rules=[]
        self.sentences=[]
        self.nonTerminalsOverall=set()
        self.notNonTerminals=set()
        self.nonTerminals=set()

    def parseRulesFile(self):
        print "Yes here"

        with open(self.rulesFile, "r") as ins:
            array = []
            for line in ins.readlines():
                splits=line.split("\r")
                for i in range(0,len(splits)):
                    splits2=splits[i].split(" ")
                    self.rules.append(splits2)
                    for j in range(0,len(splits2)-1):
                        self.nonTerminalsOverall.add(splits2[j])

        print "\nRules are updated after parsing the file \n",self.rules
        print "\nNon-Terminals also updated\n",self.nonTerminalsOverall
        return self.rules;



    def parseSentsFile(self):
        print "Yes here"

        with open(self.sentenceFile, "r") as ins:
            array = []
            for line in ins.readlines():
                splits=line.split("\r")
                for i in range(0,len(splits)):
                    splits2=splits[i].split(" ")
                    self.sentences.append(splits2)
                    for j in range(0,len(splits2)):
                        self.notNonTerminals.add(splits2[j])

        print "Sentences are updated after parsing the file \n",self.sentences

        return self.sentences;