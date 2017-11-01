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
        self.bp=dict(dict(dict()))
        self.setRulesDict(self.rulesList)
        #print self.rules   # a dictionary is created for all the rules for quicker access








    def setRulesDict(self,rules):
        #print "Setting up rules dictionary"
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
                    #print "Setup prob ",p
                else:
                    self.pi[i][i+1][X]=0
                    #print "Setup prob ",0

    def printBeautiful(self):
        print "\nBeautifully Printing Results\n"
        print "\nSentence Under Consideration\n",self.s

        print self.pi
        for k in range(0,len(self.s)):
             for j in range(0,len(self.s)-1):
                 print "\n"
                 if j+k+1<=len(self.s):
                     print "Span:",
                     for k1 in range(j,j+k+1):
                         print self.s[k1]," ",
                     print "\n"


        print self.pi



    def startCKY(self):
        self.setup()
        #first diagonal is printing correctly
        #print "Pi after setup"
        #print the first diagonal

        for i in range(0,len(self.s)):
            print i," , ",i+1," = ",self.pi[i][i+1]

        for i in range(0,len(self.s)):
            # for A in self.nonTerminals:
            #     #if A -> words[i] in grammar
            #     b=self.checkIfRuleChangesAToWord(A,self.s[i])
            #     if b!=-1:
            #         #print "Yes a rule from ",A," to ",self.s[i], ' probability ',b
            #         # if i not in self.pi:
            #         #     self.pi[i]=dict()
            #         # if i+1 not in self.pi[i]:
            #         #     self.pi[i][i+1]=dict()
            #         self.addIfNull(i,i+1,A)
            #
            #         self.pi[i][i+1][A]=b
            #     elif b==-1:
            #         #print "No a rule from ",A," to ",self.s[i]
            #         if i not in self.pi:
            #             self.pi[i]=dict()
            #         if i+1 not in self.pi[i]:
            #             self.pi[i][i+1]=dict()
            #
            #         self.pi[i][i+1][A]=0
            self.handleUnaries(i,i+1)
        # print self.pi
        # print self.bp
        self.startCKYRec()



        # print "Results\n"
        #
        # print "Pi is \n"
        # print self.pi
        #
        # print self.s
        # print self.N
        #
        # print self.bp

        self.printBeautiful()



    def startCKYRec(self):
        for span in range(2,len(self.s)):
            for begin in range(0,len(self.s)-span):
                end=begin+span
                for split in range(begin+1,end):
                    for A in self.nonTerminals:
                        for B in self.nonTerminals:
                            for C in self.nonTerminals:
                                prob = float(self.pi[begin][split][B])*float(self.pi[split][end][C])*float(self.AGoesToBCInGrammar(A,B,C))
                                self.addIfNull(begin,end,A)
                                if prob > self.pi[begin][end][A]:
                                    self.pi[begin][end][A]=prob
                                    if begin not in self.bp:
                                        self.bp[begin]=dict()
                                    if end not in self.bp[begin]:
                                        self.bp[begin][end]=dict()
                                    self.bp[begin][end][A]=(split,B,C)
                self.handleUnaries(begin,end)



    #works correctly
    def AGoesToBCInGrammar(self,A,B,C):
        if A in self.rules:
            #print " A ",A
            for list in self.rules[A]:
                #print list
                #print "Searching for prob of transformation of A ",A," to B ",B," and C ",C," in list ",list
                if (list[0]==B and list[1]==C) or (list[0]==C and list[1]==B):
                    print "Probability of transformation of ",A," to ",B," , ",C," is ",list[-1]
                    return list[-1]
        return -1

    def addIfNull(self,i,j,B):
        if i not in self.pi:
            self.pi[i]=dict()
        if j not in self.pi[i]:
            self.pi[i][j]=dict()
        if B not in self.pi[i][j]:
            self.pi[i][j][B]=float(0.0)

    #works correctly, i=start and j=end
    def handleUnaries(self,i,j):
        added=True
        while added==True:
            added=False
            for A in self.nonTerminals:
                for B in self.nonTerminals:
                    #print "WOW!! ",A,B,"\n"
                    p=self.AGoesToBInGrammarUnary(A,B)
                    self.addIfNull(i,j,B)
                    if float(self.pi[i][j][B])>=0 and float(p)>=0:
                        # print "Lol \n",p
                        # print "Lol1 \n",self.pi[i][j]
                        # print "B \n",B

                        prob = float(p)*float(self.pi[i][j][B])
                        if prob > float(self.pi[i][j][A]):
                            self.pi[i][j][A] = prob
                            if i not in self.bp:
                                self.bp[i]=dict()
                            if j not in self.bp[i]:
                                self.bp[i][j]=dict()
                            self.bp[i][j][A] =B
                            added = True


    #Works correctly

    # def AGoesToBInGrammar(self,A,B):
    #     if A in self.rules:
    #         #print " A ",A
    #         for list in self.rules[A]:
    #             #print list
    #             #print " B ",B
    #             for B1 in list:
    #                 if B1==B:
    #                     #print "Yes ", A, " transforms to ",B," in grammar"
    #                     return list[-1]
    #     return -1

    def AGoesToBInGrammarUnary(self,A,B):
        if A in self.rules:
            #print " A ",A
            for list in self.rules[A]:
                #print list
                #print " B ",B
                if len(list)==2:
                    for B1 in list:
                        if B1==B:
                            #print "Yes ", A, " transforms to ",B," in grammar"
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


