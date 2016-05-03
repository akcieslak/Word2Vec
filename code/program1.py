# Program 1:
# A program that parses, two columns: the word, word count (sort by word count descending) 
# spit out the file. anyone can pick out the words that they want to analyze. 
# (Allow parameter to get top words)

import gensim
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from gensim.models import Word2Vec
import os.path
import nltk
from nltk.corpus import stopwords
import en
import string
import operator
from nltk.stem.wordnet import WordNetLemmatizer
import csv
import sys


VAR_FILENAME = raw_input("Please enter a filename (Please include extension): ")

class Value:
    def __init__ (self, word, sentenceNum, sentenceInd):
        self.word = word
        self.count = 1
        self.sentenceArray = [(sentenceNum, sentenceInd)]
        self.avgPol = 0
        self.avgSub = 0

    def update(self, sentenceNum, sentenceInd):
        self.count += 1
        self.sentenceArray.append((sentenceNum, sentenceInd))

    def getCount(self):
        return self.count

    def getWord(self):
        return self.word


try: 
    with open(VAR_FILENAME, 'r') as FILE2:
	   TEXT = FILE2.read()
except IOError as detail:
    print "Sorry, could not find filename: " + VAR_FILENAME
    sys.exit()

CACHEDSTOPWORDS = stopwords.words('english')
PUNCTUATION = string.maketrans(string.punctuation, ' ' * len(string.punctuation))

DICTIONARY = {}
POSITION = 0
DATA = []


splitFile = []
sentences = TEXT.split(".")
wnl = WordNetLemmatizer();


for i in range(len(sentences)):
    line = sentences[i].translate(PUNCTUATION)
    line = line.decode('utf-8')
    line = line.split(' ');
    r = 0
    for point in line:
        lword = point.lower()
        lword = wnl.lemmatize(lword, pos='v')
        if lword not in CACHEDSTOPWORDS:
            if lword != '' and lword != "re":
                if (len(lword) > 1):
                    if (lword in DICTIONARY):
                        DICTIONARY[lword].update(i, r)
                    else:
                        temp = Value(lword, i, r)
                        DICTIONARY[lword] = temp
                
        r += 1

cmpfun = operator.attrgetter("count")
sortedDict = sorted(DICTIONARY.values(), key=cmpfun, reverse = True)

VAR_OUTPUT = raw_input("Enter an output file(no extension): ");
with open(VAR_OUTPUT + '.csv', 'wb') as c:
	writer = csv.writer(c)
	writer.writerow(['Word', 'Word Count']);
	j = 0
	while j < len(sortedDict):
		try: 
			writer.writerow([sortedDict[j].word.encode('utf-8'), sortedDict[j].count])
		except KeyError:
			writer.writerow([sortedDict[j].encode('utf-8'), "null"])        
		j += 1













