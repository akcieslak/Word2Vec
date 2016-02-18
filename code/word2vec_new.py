import gensim
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from gensim.models import Word2Vec
import os.path
#import enchant
import nltk
from nltk.corpus import stopwords
import en
import string
import operator



class Value:
    def __init__ (self, word, position, sentenceNum, sentenceInd):
        self.word = word
        self.count = 1
        self.positionArray = [position]
        self.sentenceArray = [(sentenceNum, sentenceInd)]
        self.avgPol = 0
        self.avgSub = 0

    def update(self, position, sentenceNum, sentenceInd):
        self.count += 1
        self.positionArray.append(position)
        self.sentenceArray.append((sentenceNum, sentenceInd))

    def getCount(self):
        return self.count

    def getPositionArray(self):
        return self.positionArray

    def getWord(self):
        return self.word

    def getSentenceArray(self):
        return self.sentenceArray

    def setAvgPol(self, avg):
        self.avgPol = avg

    def getAvgPol(self):
        return self.avgPol

    def setAvgSub(self, avg):
        self.avgSub = avg

    def getAvgSub(self):
        return self.avgSub

with open(os.path.dirname(os.path.abspath(__file__)) + '/../data/testText.txt', 'r') as FILE:
   data = FILE.read()


#Another option: take out the stop words and then tokenize each word and pass it through
#try to also use stemming and lemmatization: are, is --> be. Article:

#Finding the 50 most common words. Exclusing stop words:
SIZE = 50
#d = enchant.Dict("en_US")
with open(os.path.dirname(os.path.abspath(__file__)) + '/../data/testText.txt', 'r') as FILE2:
	text = FILE2.read()

CACHEDSTOPWORDS = stopwords.words('english')
PUNCTUATION = string.maketrans(string.punctuation, ' ' * len(string.punctuation))

DICTIONARY = {}
POSITION = 0

splitFile = []
sentences = text.split(".")


for i in range(len(sentences) - 1):
    line = sentences[i].translate(PUNCTUATION)
    line = line.decode('utf-8')
    line = line.split(' ');
    r = 0
    for point in line:
        lword = point.lower()
        POSITION += 1
        lword = en.noun.singular(lword)
        if lword not in CACHEDSTOPWORDS:
            if lword != '' and lword != "re":
                if (len(lword) > 1):
                    try:
                        lword = en.verb.present(lword)
                        lword = en.verb.infinitive(lword)
                    except Exception:
                        pass
                    if (lword in DICTIONARY):
                        DICTIONARY[lword].update(POSITION, i, r)
                    else:
                        temp = Value(lword, POSITION, i, r)
                        DICTIONARY[lword] = temp
                
        r += 1




cmpfun = operator.attrgetter("count")
sortedDict = sorted(DICTIONARY.values(), key=cmpfun, reverse = True)

topWords = []
j = 0
while j < SIZE:
    topWords.append(sortedDict[j])
    print sortedDict[j].getWord()
    j += 1




#Uses Word2Vec with original file
fd1 = nltk.FreqDist(word_tokenize(data.decode('utf-8')))
freq = sorted(list(set(fd1.values())), reverse=True)
max_min_count = freq[1]
print "FD1"
print
print
print max_min_count
print fd1.most_common(10)
for word in fd1.most_common(10):
    print word[0]


print
print
print "WORD2VEC MODEL"
sentences = sent_tokenize(data.decode('utf-8'))
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


# model = gensim.models.Word2Vec();
# model.build_vocab(tokenized_sentences);
# model.train(tokenized_sentences);
model = gensim.models.Word2Vec(tokenized_sentences, min_count=10)

word = 'school'
print "Top five most similar words to: " + word
print model.most_similar(word, topn = 5)


#print model.doesnt_match("breakfast cereal dinner lunch".split())
print model.similarity('school', 'opportunities')