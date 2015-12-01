import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from gensim.models import Word2Vec

with open('test.txt', 'r') as FILE:
    data = FILE.read()

fd1 = nltk.FreqDist(word_tokenize(data.decode('utf-8')))
freq = sorted(list(set(fd1.values())), reverse=True)
max_min_count = freq[1]
print max_min_count

sentences = sent_tokenize(data.decode('utf-8'))
tokenized_sentences = []
for sentence in sentences:
    words = word_tokenize(sentence)
    tokenized_sentences.append(words)
    

model = Word2Vec(tokenized_sentences, size=100, min_count=max_min_count)
print model.vocab
