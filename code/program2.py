# Program 1:
# after learning the whole word2vec model, (training should include stop words), feed in the words 
# you pick from the first program
# generate: for each of the ten words, find the most 5 similar and for each of the 5 look at the 2 
# most similar --> 3 columns: word from the ten words, 5 most similar to original, 2 most similar to 
# the 5
import networkx as nx
import matplotlib.pyplot as plt
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
import networkx.drawing.nx_pydot



# Reads in the same text file from program1 and builds the Word2Vec model


class Tree:
    def __init__ (self, original, bool):
        self.original = original
        self.bool = bool
        self.children = False;

    def add_children(self, children):
        self.children = children;

    def get_children(self):
        return self.children

    def get_original(self):
        return self.original

    def set_bool(self, bool):
        self.bool = bool

    def get_bool(self, bool):
        return self.bool

    def get_name(self):
        return self.original



VAR_FILENAME = raw_input("Please enter a filename **same as first prog** (Please include extension): ")
MIN_COUNT = int(raw_input("Enter a mincount depending on size of your file: "))
FILENAME = os.path.dirname(os.path.abspath(__file__)) + '/../data/' + VAR_FILENAME

try: 
    with open(VAR_FILENAME, 'r') as FILE2:
	   TEXT = FILE2.read()
except IOError as detail:
    print "Sorry, could not find filename: " + VAR_FILENAME
    sys.exit()



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

#for example the input.txt file in github
VAR_WORDS = raw_input("Enter a file with inputs for the Word2Vec model: ")

try: 
    with open(VAR_WORDS, 'r') as FILE3:
	   LIST = FILE3.read()
except IOError as detail:
    print "Sorry, could not find filename: " + VAR_WORDS
    sys.exit()

sentences = LIST.split(", ")


TOP_WORDS = []
for word in sentences:
	TOP_WORDS.append(word)

for word in TOP_WORDS:
    print word

VAR_OUTPUT = raw_input("Enter an output file(no extension): ")


with open(VAR_OUTPUT + '.csv', 'wb') as c:
    writer = csv.writer(c)
    writer.writerow(['Original Word', '5 Most Similar Words', '2 Most Similar Words'])
    trees = []
    for word in TOP_WORDS:
        writer.writerow([word, " ", " "]);
        tmp1 = []
        try: 
            for case1 in model.most_similar(word, topn=5):
                try:
                    writer.writerow([" ", case1[0].encode('utf-8')])
                except KeyError:
                    writer.writerow([" ", "null"])

                tmp2 = []
                for case2 in model.most_similar(case1[0], topn=2):
                    tmp2.append(Tree(case2[0], False))
                    try:
                        writer.writerow([" ", " ", case2[0].encode('utf-8')])
                    except KeyError:
                        writer.writerow([" ", " ", "null"])
                node = Tree(case1[0], True)
                node.add_children(tmp2)
                tmp1.append(node)
        except KeyError:
            writer.writerow([" ", " ", " "])      
        node1 = Tree(word, True)
        node1.add_children(tmp1)
        trees.append(node1)
        



#This is to draw the tree graphs
#error in prog="dot" / graphviz_layout
for thing in trees:
    # G = nx.Graph()
    G=nx.DiGraph()
    G.add_node(thing.get_name())
    for thing1 in thing.get_children():
        G.add_edge(thing.get_name(), thing1.get_name())
        for thing2 in thing1.get_children():
            G.add_edge(thing1.get_name(), thing2.get_name())
    # nx.write_dot(G,'test.dot')
    pos=nx.graphviz_layout(G, prog="dot")
    nx.draw(G,with_labels=True,arrows=True)
    plt.savefig(thing.get_name() + ".png")
    # nx.draw_graphviz(G)
    # write_dot(G,thing.get_name() + ".png" )




















