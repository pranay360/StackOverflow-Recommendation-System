import time, re, json, numpy as np, sys, csv
from PyQt5.QtGui import *
from PyQt5.Qt import *
try:
    from PyQt4.QtCore import QString
except ImportError:
    QString = str
from maingui import Ui_MainWindow
from recgui import Ui_Dialog
from sklearn.svm import LinearSVC
from nltk.corpus import stopwords
from sklearn.pipeline import Pipeline
from sklearn.externals import joblib
from nltk.stem.snowball import SnowballStemmer
from sklearn.multiclass import OneVsRestClassifier
from sklearn.metrics import f1_score
from sklearn.metrics import accuracy_score
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
import pandas as pd

s=set(stopwords.words('english'))
stemmer = SnowballStemmer('english', ignore_stopwords=True)
fh=open('Tags.txt','r')
fh2=open('cleaned.txt','r')
_i=[]
_t=[]
_T=[]
_b=[]
count=0
tagrows=fh.read().split('\n')[:500000]
checktags=[]
X=fh2.read().split('\n')[:500000]
classifier = joblib.load('clf.txt')
multibin = joblib.load('multibin.txt')
vectorizer_2=CountVectorizer()

class SO(QMainWindow,Ui_MainWindow):
	def __init__(self, parent=None):
		super(SO, self).__init__(parent)
		self.setupUi(self)
		self.pushButton.clicked.connect(self.predictTags)
		self.pushButton_4.clicked.connect(self.recommend)
		self.pushButton_4.hide()
		self.df=pd.read_csv("trainset.csv")
		self.r1.clicked.connect(self.newwindowr1)
		self.r2.clicked.connect(self.newwindowr2)
		self.r3.clicked.connect(self.newwindowr3)
		self.r4.clicked.connect(self.newwindowr4)
		self.r5.clicked.connect(self.newwindowr5)
		#self.ac.clicked.connect(self.accuracy)
		#self.pushButton_3.clicked.connect(self.f1score)
		self.r1.hide()
		self.r2.hide()
		self.r3.hide()
		self.r4.hide()
		self.r5.hide()
		self.lotags.hide()
		self.otags.hide()
		self.ac.hide()
		self.acl.hide()
		self.pushButton_3.hide()
		self.lf1.hide()
		self.label_9.hide()

	def newwindowr1(self):
		self.new=RCMD(self)
		self.new.display(str(self.r1.text()))
	def newwindowr2(self):
		self.new=RCMD(self)
		self.new.display(str(self.r2.text()))
	def newwindowr3(self):
		self.new=RCMD(self)
		self.new.display(str(self.r3.text()))
	def newwindowr4(self):
		self.new=RCMD(self)
		self.new.display(str(self.r4.text()))
	def newwindowr5(self):
		self.new=RCMD(self)
		self.new.display(str(self.r5.text()))
	'''
	def f1score(self):
		otags=str(self.otags.text()).split()
		comm=set(otags)&set(self.tagarr)
		commlist=list(comm)
		if len(comm)<len(otags):
			while len(commlist)!=len(otags):
				commlist.append('ZzZzz')
		otags.sort()
		commlist.sort(reverse=True)
		print otags
		print commlist
		f1=f1_score(otags,commlist, average='micro')
		print f1
		self.pushButton_3.setText(QString(str(f1)))
	def accuracy(self):
		otags=str(self.otags.text()).split()
		comm=set(otags)&set(self.tagarr)

		commlist=list(comm)
		if len(comm)<len(otags):
			while len(commlist)!=len(otags):
				commlist.append('ZzZzz')
		otags.sort()
		commlist.sort(reverse=True)
		print otags
		print commlist
		ac=accuracy_score(otags,commlist)
		print ac
		self.ac.setText(QString(str(ac)))
	'''

	def recommend(self):
		cossim=[]
		#QApplication.processEvents()
		A=vectorizer_2.fit_transform(self.T)
		#QApplication.processEvents()
		for i,Tags in enumerate(checktags):
			if len(self.tagarr)<=3:
				if len(set(self.tagarr)&set(Tags)) > 0:
					B=vectorizer_2.transform([X[i]])
					cossim.append([i+1,cosine_similarity(A,B)[0][0]])
			else:
				if len(set(self.tagarr)&set(Tags)) > 1:
					B=vectorizer_2.transform([X[i]])
					cossim.append([i+1,cosine_similarity(A,B)[0][0]])
		#QApplication.processEvents()
		cossim.sort(key=lambda x: x[1], reverse=True)
		indexes=[x[0] for x in cossim[:5]]
		larr=[self.r1,self.r2,self.r3,self.r4,self.r5]
		temp=self.df[self.df.Id.isin(indexes)].reset_index()
		#print row['Id'],'--',row['Title'],'--',row['Tags']
		for i, row in temp.iterrows():
			larr[i].setText(QString(row['Title']))
			_i.insert(0,row['Id'])
			_t.insert(0,row['Title'])
			_T.insert(0,row['Tags'])
			_b.insert(0,row['Body'])
			larr[i].show()

	def predictTags(self):
		self.T=[]
		words = str(self.lineEdit.text())+' '+str(self.plainTextEdit.toPlainText())
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
		self.T.append(words)
		results=classifier.predict(self.T)
		results=multibin.inverse_transform(results)
		print '\n',results,'\n'
		buff=''
		self.tagarr=[]
		for result in results[0]:
			buff=buff+QString(result)+' ; '
			self.tagarr.append(result)
		self.lineEdit_2.setText(buff[:len(buff)-3])
		self.recommend()

class RCMD(QDialog,Ui_Dialog):
	def __init__(self, parent=None):
		super(RCMD, self).__init__(parent)
		self.setupUi(self)
	def display(self,index):
		x=_i.index(index)
		self.label.setText('id: '+QString(_i[x]))
		self.lineEdit.setText(QString(_t[x]))
		self.lineEdit_2.setText(QString(_T[x]))
		self.plainTextEdit.setPlainText(QString(_b[x]))
		self.show()

def main(argv):
	for line in tagrows:
		checktags.append(line.split())
	app = QApplication(argv)
	window=SO()
	window.show()
	retval = app.exec_()
	sys.exit(retval)

if __name__ == '__main__':
	main(sys.argv)
