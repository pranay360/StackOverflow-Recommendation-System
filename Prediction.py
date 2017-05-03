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
	words = (raw_input("Enter Your Question: ")).lower()
	words = re.sub('\n',' ',words)
	words = re.sub('[!@%^&*()$:"?<>=~,;`{}|]',' ',words)
	words = re.sub(r'''(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'".,<>?]))''',' ',words)
	words = re.sub('_','-',words)
	words = words.replace('[',' ')
	words = words.replace(']',' ')
	words = words.replace('/',' ')
	words = words.replace('\\',' ')
	words = re.sub(r'(\s)\-+(\s)',r'\1', words)
	words = re.sub(r'\.+(\s)',r'\1', words)
	words = re.sub(r'\.+\.(\w)',r'\1', words)
	words = re.sub(r'(\s)\.+(\s)',r'\1', words)
	words = re.sub("'",'', words)
	words = re.sub(r'\s\d+[\.\-\+]+\d+|\s[\.\-\+]+\d+|\s+\d+\s+|\s\d+[\+\-]+',' ',words)
	words = re.sub("^\d+\s|\s\d+\s|\s\d+$"," ", words)
	words = re.sub(r'\s\#+\s|\s\++\s',' ',words)	
	stemmed_words = [stemmer.stem(word) for word in words.split()]
	clean_text = filter(lambda w: not w in s,stemmed_words)
	words=''
	for word in clean_text:
		words+=word+' '
	T.append(words)
	print '\n',classifier.predict(T),'\n'
	c=input("Continue?\nPress 0 to Quit: ")
	if c is 0:
		break
		
print "Exiting..."
fh.close()
fh2.close()
