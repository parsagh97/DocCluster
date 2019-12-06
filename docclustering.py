# -*- coding: utf-8 -*-
"""DocClustering.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Dtgp20wzB5KuAThaXJaOTIqRI9eD74v7
"""

pip install mpld3

import numpy as np
import pandas as pd
import nltk
import re
import os
import codecs
from sklearn import feature_extraction
import mpld3

PATH = "/"
dir_path = os.listdir(PATH)
papers_list = list()
for item in dir_path:
    if ".txt" in item:
        papers_list.append(item)

print(papers_list)

doc_word = list()

for i in range(len(papers_list)):
  doc_word.append(open(PATH +"/"+ papers_list[i]).read())

index = list()
for i in range(len(papers_list)):
  index.append(i)

from bs4 import BeautifulSoup

nltk.download('stopwords')
nltk.download('punkt')

from nltk.stem.snowball import SnowballStemmer
stemmer = SnowballStemmer("english")

def tokenize_and_stem(text):
    tokens = [word for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]
    filtered_tokens = []
    for token in tokens:
        if re.search('[a-zA-Z]', token):
            filtered_tokens.append(token)
    stems = [stemmer.stem(t) for t in filtered_tokens]
    return stems

def tokenize_only(text):
    tokens = [word.lower() for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]
    filtered_tokens = []
    for token in tokens:
        if re.search('[a-zA-Z]', token):
            filtered_tokens.append(token)
    return filtered_tokens

totalvocab_stemmed = []
totalvocab_tokenized = []
for i in doc_word:
    allwords_stemmed = tokenize_and_stem(i)
    totalvocab_stemmed.extend(allwords_stemmed)
    
    allwords_tokenized = tokenize_only(i)
    totalvocab_tokenized.extend(allwords_tokenized)

vocab_frame = pd.DataFrame({'words': totalvocab_tokenized}, index = totalvocab_stemmed)

from sklearn.feature_extraction.text import TfidfVectorizer

tfidf_vectorizer = TfidfVectorizer(max_df=0.8, max_features=200000,
                                 min_df=0.2, stop_words='english',
                                 use_idf=True, tokenizer=tokenize_and_stem, ngram_range=(1,3))

tfidf_matrix = tfidf_vectorizer.fit_transform(doc_word)

print(tfidf_matrix.shape)

terms = tfidf_vectorizer.get_feature_names()

from sklearn.metrics.pairwise import cosine_similarity
dist = 1 - cosine_similarity(tfidf_matrix)

from sklearn.cluster import KMeans
num_clusters = 10
km = KMeans(n_clusters=num_clusters)
km.fit(tfidf_matrix)
clusters = km.labels_.tolist()

pip install joblib

from sklearn.externals import joblib

joblib.dump(km,'doc_cluster.pkl')
km = joblib.load('doc_cluster.pkl')
clusters = km.labels_.tolist()

import pandas as pd
papers = {'papers_list':papers_list, 'index':index, 'cluster':clusters}
frame = pd.DataFrame(papers, index=[clusters], columns=['index', 'papers_list', 'cluster'])

frame['cluster'].value_counts()

grouped = frame['index'].groupby(frame['cluster'])
grouped.mean()

import os 

import matplotlib.pyplot as plt
import matplotlib as mpl

from sklearn.manifold import MDS

MDS()

mds = MDS(n_components=2, dissimilarity="precomputed", random_state=1)

pos = mds.fit_transform(dist)  

xs, ys = pos[:, 0], pos[:, 1]

# Commented out IPython magic to ensure Python compatibility.
cluster_colors = {0: 'red', 1: 'blue', 2: 'green', 3: 'gray', 4: 'yellow', 5:'brown', 6:'gray', 7:'brown', 8:'orange', 9:'black'}
# %matplotlib inline

df = pd.DataFrame(dict(x=xs, y=ys, label=clusters, title=papers_list)) 
groups = df.groupby('label')
fig, ax = plt.subplots(figsize=(17, 9)) 
ax.margins(0.05) 
for name, group in groups:
    ax.plot(group.x, group.y, marker='o', linestyle='', ms=12, color=cluster_colors[name], mec='none')
    ax.set_aspect('auto')
    ax.tick_params(\
        axis= 'x',          
        which='both',      
        bottom='off',      
        top='off',         
        labelbottom='off')
    ax.tick_params(\
        axis= 'y',         
        which='both',      
        left='off',      
        top='off',       
        labelleft='off')
    
ax.legend(numpoints=1)  

for i in range(len(df)):
    ax.text(df.ix[i]['x'], df.ix[i]['y'], df.ix[i]['title'], size=8)  
    
plt.show()
plt.savefig('clusters.png', dpi=200)
