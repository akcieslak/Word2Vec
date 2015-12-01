t = [['a', 'b', 'c'], ['d', 'a', 'e']]

# In[3]:

from gensim.models import Word2Vec


# In[ ]:

model = Word2Vec(t, min_count=1)


# In[17]:

print model.vocab

