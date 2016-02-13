import json, HTMLParser, re, nltk, csv, sys, stackexchange
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from collections import defaultdict
from nltk.stem.snowball import SnowballStemmer

ft=open('TTags.txt','w')
fh=open('Tcleaned.txt','w')
fi=open('Tid.txt','w')
s=set(stopwords.words('english'))
html_parser= HTMLParser.HTMLParser()
so = stackexchange.Site(stackexchange.StackOverflow)
so.be_inclusive()
i=0

#no. of rows 5547983

for question in so.questions(pagesize=10):
	try:
		t=str(question.title.lower())
		b=str(question.body.lower())
		z=str(html_parser.unescape(str(b.encode('utf-8'))))
		tags=str(question.tags)
		_id=question.id
		f=0
		bd=''
		while f<len(z):
			x=z.find("<p>",f)
			y=z.find("</p>",f)
			bd=''
			if x>=0 and y>=0:
				s1=[]
				s2=[]
				s3=[]
				s4=[]
				s1=[m.start() for m in re.finditer('<code>', z[x:y])]
				s2=[m.start() for m in re.finditer('</code>', z[x:y])]
				r=0
				lh=0
				while r<len(s1) and r<len(s2):
					z=z.replace(z[s1[r]-lh:s2[r]+7-lh],'')
					lh=lh+len(z[s1[r]-lh:s2[r]+7-lh])
					r=r+1
				r=0
				y=z.find("</p>",f)
				s3=[m.start() for m in re.finditer('<a h', z[x:y])]
				s4=[m.start() for m in re.finditer('</a>', z[x:y])]
				lh=0
				while r<len(s3) and r<len(s4):
					z=z.replace(z[s3[r]-lh:s4[r]+4-lh],'')
					lh=lh+len(z[s3[r]-lh:s4[r]+4-lh])
					r=r+1
				bd+=str(z[x+3:y].encode('utf8'))+' '
				f=y+5
			else:
				break
		words=re.sub('[!@%^&*()$:"?<>=~,;`{}|]',' ',t.lower()+' '+bd)
		words=re.sub(r'''(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'".,<>?]))''',' ',words)
		words=re.sub('\n',' ',words)
		words=re.sub('_','-',words)
		words=words.replace('[',' ')
		words=words.replace(']',' ')
		words=words.replace('/',' ')
		words=words.replace('\\',' ')
		words = re.sub(r'(\s)\-+(\s)',r'\1', words)
		words = re.sub(r'\.+(\s)',r'\1', words)
		words = re.sub(r'\.+\.(\w)',r'\1', words)
		words = re.sub(r'(\s)\.+(\s)',r'\1', words)
		words = re.sub("'",'', words)
		words = re.sub(r'\s\d+[\.\-\+]+\d+|\s[\.\-\+]+\d+|\s+\d+\s+|\s\d+[\+\-]+',' ',words)
		words= re.sub("^\d+\s|\s\d+\s|\s\d+$"," ", words)
		words= re.sub(r'\s\#+\s|\s\++\s',' ',words)
		stemmer = SnowballStemmer("english", ignore_stopwords=True)
		stemmed_words = [stemmer.stem(word) for word in words.split()]
		clean_text=filter(lambda w: not w in s,stemmed_words)
		words=''
		for word in clean_text:
			words+=word+' '
		fh.write(words+'\n')
		for tag in tags:
			ft.write(tag+' ')
		ft.write('\n')
		fi.write(str(_id))
		print "Post Cleaned-",_id
		i=i+1		
	except Exception,e:
		print "EXCEPTION: ",str(e)
		pass
		
fh.close()
fi.close()
ft.close()

print
print
print
print "CLEANING COMPLETED"
print i," Posts Cleaned."
print
