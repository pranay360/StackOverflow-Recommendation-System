from sklearn.externals import joblib
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC
from sklearn.multiclass import OneVsRestClassifier
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.preprocessing import MultiLabelBinarizer
tags={}
freq=[]
count=0
fh=open('Tags.txt','r')
fh2=open('cleaned.txt','r')
tagrows=fh.read().split('\n')[:500000]
X=fh2.read().split('\n')[:500000]
Y = [[] for i in range(len(X))]
classifier = Pipeline([
		     ('vectorizer', CountVectorizer()),
		     ('tfidf', TfidfTransformer()),
		     ('clf', OneVsRestClassifier(LinearSVC(), n_jobs = -2))])
for line in tagrows:
	for tag in line.split():
		if tag in tags:
			tags[tag]+=1
		else:
			tags[tag]=1
	count=0
for tag in sorted(tags,key=lambda tag:tags[tag], reverse=True):
	if tags[tag] > 4000:
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

multibin=MultiLabelBinarizer()
Y=multibin.fit_transform(Y)
classifier.fit(X,Y)
job = joblib.dump(classifier, 'clf.txt', compress=9)
job = joblib.dump(multibin, 'multibin.txt', compress=9)
