# Word2Vec
I am currently working with Word2Vec to find similarity between words. First, I read in data and parse it to find the 50 most common
words in the data. Then I use the Word2Vec model to find the most similar words to each word in the top 50 list. 

There are currently two python files: word2vec.py and word2vec_new.py. 
word2vec.py: Uses the Word2Vec model with the original data that was given
word2vec_new.py: Uses the Word2Vec model with the patsed original data (takes out stop words and unnecessary additions to text)
