import time, re, json, numpy as np
from sklearn.svm import LinearSVC
from nltk.corpus import stopwords
from sklearn.pipeline import Pipeline
from nltk.stem.snowball import SnowballStemmer
from sklearn.multiclass import OneVsRestClassifier
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer

s=set(stopwords.words('english'))
stemmer = SnowballStemmer("english", ignore_stopwords=True)
fh=open('Tags.txt','r')
fh2=open('cleaned.txt','r')
fh3=open('TTags.txt', 'r')
fh4=open('Tcleaned.txt','r')
tags={}
freq=[]
count=0
tagrows=fh.read().split('\n')[:500000]
X=fh2.read().split('\n')[:500000]
Y = [[] for i in range(len(X))]

for line in tagrows:
	for tag in line.split():
		if tag in tags:
			tags[tag]+=1
		else:
			tags[tag]=1
#34945 unique tags in 10 lakh posts

for tag in sorted(tags,key=lambda tag:tags[tag], reverse=True):
	if tags[tag] > 800:
		count += 1
		freq.append(tag)
	else:
		break

print "Training..."
for x,tag in enumerate(freq):
	i=0
	for row in tagrows:
		if tag in row.split():
			Y[i].append(tag)
		i=i+1


classifier = Pipeline([
         ('vectorizer', CountVectorizer()),
         ('tfidf', TfidfTransformer()),
         ('clf', OneVsRestClassifier(LinearSVC(class_weight='auto'), n_jobs = -2))])
classifier.fit(X,Y)
print "Ready..."


while True:
	T=[]
	words = fh.readline().lower().replace(' \n','')
	T.append(words)
	print '\n',classifier.predict(T),fh3.readline(),'\n'
	
		
print "Exiting..."
fh.close()
fh2.close()
