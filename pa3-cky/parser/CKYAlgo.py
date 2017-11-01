from GrammarParser import GrammarParser


class CKY:

    def __init__(self,rulesFile,sentenceFile):


        self.grammarParser=GrammarParser(rulesFile,sentenceFile)

        self.rulesList=self.grammarParser.parseRulesFile()
        self.sentences=self.grammarParser.parseSentsFile()

        self.rules=dict()
        self.nonTerminals=self.grammarParser.nonTerminals

        self.s=None    #list of words in each line
        self.N=len(self.grammarParser.nonTerminals)  #non terminal words
        self.pi=dict(dict(dict()))
        self.pi_track=dict(dict(dict()))
        self.bp=dict(dict(dict()))
        self.setRulesDict(self.rulesList)





    def setRulesDict(self,rules):
        for list in rules:
            if list!=None and len(list)>=3:
                key=list[0]
                if key not in self.rules:
                    self.rules[key]=[]
                self.rules[key].append(list[1:])



    def checkIfRuleChangesAToWord(self,A,word):
        if A in self.rules:  #key A is in dictionary
            for list in self.rules[A]:
                if list[0]==word:
                    return list[-1]
        return -1

    #sets up diagonal of the matrix
    def setup(self):
        for i in range(0,len(self.s)):
            for X in self.nonTerminals:
                self.addIfNull(i,i+1,X)

                p=self.AGoesToBInGrammarUnary(X,self.s[i])
                if p>=0:
                    self.pi[i][i+1][X]=p
                    str1=str(X)+"->"+str(self.s[i])
                    self.pi_track[i][i+1][X]=str1
                else:
                    self.pi[i][i+1][X]=0

    def printBeautiful(self):
        print "\nSentence Under Consideration\n",self.s
        print self.pi
        for k in range(0,len(self.s)):
             for j in range(0,len(self.s)):
                 print "\n"
                 posStart=j
                 posEnd=j+k+1
                 if j+k+1<=len(self.s):
                     print "Span:",
                     for k1 in range(j,j+k+1):
                         print self.s[k1]," ",
                     print "\n"

                 if posEnd in self.pi[posStart]:
                     for key in self.pi[posStart][posEnd]:
                        if self.pi_track[posStart][posEnd][key]!=None:
                            print "P(",self.pi_track[posStart][posEnd][key],")=",
                            print self.pi[posStart][posEnd][key]


    def startCKY(self):
        self.setup()
        for i in range(0,len(self.s)):
           self.handleUnaries(i,i+1)
        self.startCKYRec()
        self.printBeautiful()



    def startCKYRec(self):
        for span in range(2,len(self.s)+1):
            for begin in range(0,len(self.s)-span+1):
                end=begin+span
                for split in range(begin+1,end):
                    for A in self.nonTerminals:
                        for B in self.nonTerminals:
                            for C in self.nonTerminals:
                                prob = float(self.pi[begin][split][B])*float(self.pi[split][end][C])*float(self.AGoesToBCInGrammar(A,B,C))
                                self.addIfNull(begin,end,A)
                                if prob > self.pi[begin][end][A]:
                                    self.pi[begin][end][A]=prob
                                    str1=str(A)+"->"+str(B)+" , "+str(C)
                                    self.pi_track[begin][end][A]=str1
                                    if begin not in self.bp:
                                        self.bp[begin]=dict()
                                    if end not in self.bp[begin]:
                                        self.bp[begin][end]=dict()
                                    self.bp[begin][end][A]=(split,B,C)
                self.handleUnaries(begin,end)



    #works correctly
    def AGoesToBCInGrammar(self,A,B,C):
        if A in self.rules:
            for list in self.rules[A]:
                if (list[0]==B and list[1]==C) or (list[0]==C and list[1]==B):
                    return list[-1]
        return -1

    def addIfNull(self,i,j,B):
        if i not in self.pi:
            self.pi[i]=dict()
        if j not in self.pi[i]:
            self.pi[i][j]=dict()
        if B not in self.pi[i][j]:
            self.pi[i][j][B]=float(0.0)

        if i not in self.pi_track:
            self.pi_track[i]=dict()
        if j not in self.pi_track[i]:
            self.pi_track[i][j]=dict()
        if B not in self.pi_track[i][j]:
            self.pi_track[i][j][B]=None

    #works correctly, i=start and j=end
    def handleUnaries(self,i,j):
        added=True
        while added==True:
            added=False
            for A in self.nonTerminals:
                for B in self.nonTerminals:
                    p=self.AGoesToBInGrammarUnary(A,B)
                    self.addIfNull(i,j,B)
                    if float(self.pi[i][j][B])>=0 and float(p)>=0:
                        prob = float(p)*float(self.pi[i][j][B])
                        if prob > float(self.pi[i][j][A]):
                            self.pi[i][j][A] = prob
                            str1=str(A)+"->"+str(B)
                            self.pi_track[i][j][A]=str1
                            if i not in self.bp:
                                self.bp[i]=dict()
                            if j not in self.bp[i]:
                                self.bp[i][j]=dict()
                            self.bp[i][j][A] =B
                            added = True




    def AGoesToBInGrammarUnary(self,A,B):
        if A in self.rules:
            for list in self.rules[A]:
                if len(list)==2:
                    for B1 in list:
                        if B1==B:
                            return list[-1]
        return -1


def main():

    rulesFile='../grammar_rules.txt'
    sentencesFile='../sents.txt'

    cky = CKY(rulesFile,sentencesFile)


    #for i in range(0,len(cky.sentences)):
    cky.s=cky.sentences[0]
    cky.startCKY()


if __name__ == "__main__":
    main()


