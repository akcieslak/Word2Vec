import gensim
from gensim.models import Word2Vec
from gensim.models.word2vec import LineSentence
import codecs


f = open('test.rtf', 'r')
text = f.read()
sentences1 = text.split(".")
sentences2 = []


list1 = [['this','dog'],['cool','dog']]

##class MySentences(object):
##    def __init__(self, file):
##        self.file = file
##
##    def __iter__(self):
##        for line in open(file):
##            yield line.split()

#sentences3 = LineSentence('test.rtf')

for line in sentences1:
    line = codecs.decode(line, "utf-8")
    line = line.strip()
    temp = line.split(" ")
    wordList = []
    for word in temp:
        if word != '':
            wordList += [word]
    sentences2 += [wordList]


print sentences2


#word2vec = Word2Vec()
#model = word2vec.fit(sentences2)


#model = gensim.models.Word2Vec(sentences2)
#print model['student']

#model = Word2Vec(sentences2, min_count=10)
#model.build_vocab(sentences2)
#model.train(sentences2)

#sentences2 = MySentences('test.txt')
model = gensim.models.Word2Vec(sentences2, size = 100)





