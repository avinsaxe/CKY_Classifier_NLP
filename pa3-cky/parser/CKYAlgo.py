from GrammarParser import GrammarParser


class CKY:

    def __init__(self,s1,n1,nonTerms,rules):
        self.pi=None
        self.s=s1    #list of words in each line
        self.N=n1  #non terminal words
        a, b, c = len(self.s)+1, len(self.s)+1, n1
        self.pi=dict(dict(dict()))
        self.bp=dict(dict(dict()))
        self.nonTerminals=nonTerms
        self.rules=dict()
        self.setRulesDict(rules)
        self.grammarParser=GrammarParser('../grammar_rules.txt','../sents.txt')
        print self.rules   # a dictionary is created for all the rules for quicker access





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

    def setup(self):
        for i in range(0,len(self.s)):
            for X in self.nonTerminals:
                self.addIfNull(i,i,X)
                p=self.AGoesToBInGrammar(X,self.s[i])
                if p>=0:
                    self.pi[i][i][X]=p
                    #print "Setup prob ",p
                else:
                    self.pi[i][i][X]=0
                    #print "Setup prob ",0

    def startCKY(self):
        self.setup()
        print self.pi
        print self.s
        print self.N
        print self.bp

        for i in range(0,len(self.s)):
            for A in self.nonTerminals:
                #if A -> words[i] in grammar
                b=self.checkIfRuleChangesAToWord(A,self.s[i])
                if b>=0:
                    #print "Yes a rule from ",A," to ",self.s[i], ' probability ',b
                    # if i not in self.pi:
                    #     self.pi[i]=dict()
                    # if i+1 not in self.pi[i]:
                    #     self.pi[i][i+1]=dict()
                    self.addIfNull(i,i+1,A)

                    self.pi[i][i+1][A]=b
                else:
                    #print "No a rule from ",A," to ",self.s[i]
                    if i not in self.pi:
                        self.pi[i]=dict()
                    if i+1 not in self.pi[i]:
                        self.pi[i][i+1]=dict()

                    self.pi[i][i+1][A]=0
            self.handleUnaries(i,i+1)
        print self.pi
        print self.bp
        self.startCKYRec()



        print "Results\n"

        print "Pi is \n"
        print self.pi

        print self.s
        print self.N

        print self.bp



    def startCKYRec(self):
        for span in range(2,len(self.s)):
            for begin in range(0,len(self.s)-span):
                end=begin+span
                for split in range(begin+1,end-1):
                    for A in self.nonTerminals:
                        for B in self.nonTerminals:
                            for C in self.nonTerminals:
                                prob = self.pi[begin][split][B]*self.pi[split][end][C]*self.AGoesToBCInGrammar(A,B,C)
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
                flag1=False
                flag2=False
                for B1 in list:
                    if B1==B:
                        flag1=True
                    if B1==C:
                        flag2=True

                if flag1 and flag2:
                    #print "Probability of transformation of ",A," to ",B," , ",C," is ",list[-1]
                    return list[-1]
        return -1

    def addIfNull(self,i,j,B):
        if i not in self.pi:
            self.pi[i]=dict()
        if j not in self.pi[i]:
            self.pi[i][j]=dict()
        if B not in self.pi[i][j]:
            self.pi[i][j][B]=0

    #works correctly, i=start and j=end
    def handleUnaries(self,i,j):
        added=True
        while added==True:
            added=False
            for A in self.nonTerminals:
                for B in self.nonTerminals:
                    #print "WOW!! ",A,B,"\n"
                    p=self.AGoesToBInGrammar(A,B)
                    self.addIfNull(i,j,B)
                    if self.pi[i][j][B]>=0 and p>=0:
                        #print "Lol"
                        prob = p*self.pi[i][j][B]
                        if prob > self.pi[i][j][A]:
                            self.pi[i][j][A] = prob
                            if i not in self.bp:
                                self.bp[i]=dict()
                            if j not in self.bp[i]:
                                self.bp[i][j]=dict()
                            self.bp[i][j][A] =B
                            added = True


    #Works correctly

    def AGoesToBInGrammar(self,A,B):
        if A in self.rules:
            #print " A ",A
            for list in self.rules[A]:
                #print list
                #print " B ",B
                for B1 in list:
                    if B1==B:
                        #print "Yes ", A, " transforms to ",B," in grammar"
                        return list[-1]
        return -1


def main():
    s=['fish','people','fish','tanks']
    nonTerms=['S','NP','VP','V@VP_V','V','PP','@VP_V','N','P']



    rules=[['S','NP','VP',0.9],
           ['S','VP',0.1],
           ['VP','V','NP',0.5],
           ['VP','V',0.1],
           ['VP','V@VP_V',0.3],
           ['VP','V','PP',0.1],
           ['@VP_V','NP','PP',1.0],
           ['NP','NP','NP',0.1],
           ['NP','NP','PP',0.2],
           ['NP','N',0.7],
           ['PP','P','NP',1.0],
           ['N','people',0.5],
           ['N','fish',0.2],
           ['N','tanks',0.2],
           ['N','rods',0.1],
           ['V','people',0.1],
           ['V','fish',0.6],
           ['V','tanks',0.3],
           ['P','with',1.0]]

   # grammerParse= GramarParser('../grammar_rules.txt','../sents.txt')



    cky = CKY(s,5,nonTerms,rules)


    rules=cky.grammarParser.parseRulesFile()
    sentences=cky.grammarParser.parseSentsFile()

    cky.startCKY()
if __name__ == "__main__":
    main()


