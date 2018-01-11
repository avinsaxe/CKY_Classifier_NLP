# CKY_Classifier_NLP
Implemented my own 3 dimension, dynamic programming implementation of CKY Classifier

### How to run the code:

##### We have 2 input files

###### 1. pa3-cky/grammar_rules.txt* 

The grammar rules file has all the grammar rules as required. If you want to add more grammar rules, you can add new rules in next lines, with each term of the rule separated by a single ‘ ’ space character.
The program is generic enough, to handle new grammar rules, given grammar rules are formatted correctly and can be parsed by the program.
pa3-cky/sents.txt

###### 2. *pa3-cky/sents.txt*

The sents.txt file, contains all the input sentences. If you want to add new sentences or replace original, you can go ahead and put all the sentences in this file.
The program will read sentences from this file alone.

###### I have two python main code files.

###### 1. pa3-cky/sents.txt 
###### 2. pa3-cky/parser/GrammarParser.py

Grammar parser file has a class named GrammarParser, which is equipped with file I/O and parse features, and can extract relevant grammar rules and also the sentences from the input file.
pa3-cky/parser/CKYAlgo.py

CKYAlgo file, has a class named CKYAlgo, which uses GrammarParser class to parse the input file and run CKY Algorithm on it.
It also prints the results in the specified format on the terminal
To run simply type the following command. It will take all the input files by default. 
python CKYAlgo.py

###### Analysis:

1. We use a dynamic programming approach, instead of greedy approach, and compute and store all possible useful states
2. We compute all the possible states in parallel before finalizing a result.
3. The dynamic programming approach stores a 3 D table, and the values are reused throughout the cycle of computation
4.  There can be instances of ambiguous parsing, where very close probabilities are reached for different possible solutions, and the ambiguity exists in the choice
5. I have used a dictionary based approach, for accessing all the relevant states of the dynamic programming approach in constant time. This has significantly improved the speed of computation
6. I have used a dictionary of list approach for storing all the rules after parsing from the rules file. This also improves searching of a particular rule for a sentence.

###### Limitations
1. There is only one format in which input grammar rules and input sentences can be given. If the format of these rules and sentences is not correct, i.e. multiple sentences in one line, or grammar rules not ending with a \n character, then the program will fail 
