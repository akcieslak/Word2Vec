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


# word2vec will take out the stop words to get the top 50 words and then train 
# word2vec with the original data or data w/o stop words (user given choice) to 
# find the first 5 similar words and their value of similarity to the top 50 words

VAR_FILENAME = raw_input("Please enter a filename (Please include extension): ")
MIN_COUNT = int(raw_input("Enter a mincount depending on size of your file: "))
FILENAME = os.path.dirname(os.path.abspath(__file__)) + '/../data/' + VAR_FILENAME


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


#Finding the 50 most common words. Excluding stop words:
SIZE = 50
try: 
    with open(FILENAME, 'r') as FILE2:
	   TEXT = FILE2.read()
except IOError as detail:
    print "Sorry, could not find filename: " + VAR_FILENAME
    sys.exit()

CACHEDSTOPWORDS = stopwords.words('english')
PUNCTUATION = string.maketrans(string.punctuation, ' ' * len(string.punctuation))

DICTIONARY = {}
POSITION = 0
DATA = []

STOP = False
VAR_TRAINING = raw_input("Would you like to filter the data before training? (Y/N)")
if (VAR_TRAINING == 'Y'):
    STOP = True;

splitFile = []
sentences = TEXT.split(".")
wnl = WordNetLemmatizer();

for i in range(len(sentences) - 1):
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
                    ## Word2Vec New
                    if (STOP == True):
                        DATA += [lword];
                    ##
                    if (lword in DICTIONARY):
                        DICTIONARY[lword].update(i, r)
                    else:
                        temp = Value(lword, i, r)
                        DICTIONARY[lword] = temp
                
        r += 1

## Using the data w/o stop words
if (STOP == True):
    with open('workingfile.txt', 'w') as f:
        for word in DATA:
            f.write(word.encode('utf-8') + " ");

    with open(os.path.dirname(os.path.abspath(__file__)) + '/workingfile.txt', 'r') as FILE2:
        NEWTEXT = FILE2.read()

    TEXT = NEWTEXT


cmpfun = operator.attrgetter("count")
sortedDict = sorted(DICTIONARY.values(), key=cmpfun, reverse = True)

## Saving the top 50 words in the topWords
topWords = []
j = 0
while j < SIZE:
    topWords.append(sortedDict[j])
    j += 1


fd1 = nltk.FreqDist(word_tokenize(TEXT.decode('utf-8')))
freq = sorted(list(set(fd1.values())), reverse=True)
max_min_count = freq[1]



sentences = sent_tokenize(TEXT.decode('utf-8'))
tokenized_sentences = []
for sentence in sentences:
    words = word_tokenize(sentence)
    tokenized_sentences.append(words)


#model = Word2Vec(sentences, size = 100, window = 5, min_count=5, workers=4)
#sentences: the sentences to train on 
#size: the dimensionality of feature vectors
#window: max distance between the current and predicted word
#min_count: ignore all words with total frequency lower than this
#workers: amount of workers used to train the model
#alpha: the initial learning rate (will linearly drop to sero as training progresses)

try:
    model = gensim.models.Word2Vec(tokenized_sentences, min_count=MIN_COUNT)
except RuntimeError:
    print "There was an error. Your min_count needs to be smaller"
    sys.exit()

VAR_OUTPUT = raw_input("Enter an output file(no extension): ")
## Getting word2vecs most similar words of the 50 most common words

with open(VAR_OUTPUT + '.csv', 'wb') as c:
    writer = csv.writer(c)
    writer.writerow(['Word', 'Similar Word', 'Value of Similarity'])
    count = 1
    for word in topWords:
        try :
            writer.writerow([word.getWord().encode('utf-8')])
            for case in model.most_similar(word.getWord(), topn = 5):
                writer.writerow([" ", case[0], case[1]])
        except KeyError :
            writer.writerow([word.getWord().encode('utf-8'), "null"])        

        count += 1

