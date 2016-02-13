import stackexchange, json, HTMLParser, re, nltk
from nltk.corpus import stopwords
from bs4 import BeautifulSoup
from collections import defaultdict

s=set(stopwords.words('english'))
fh = open("stackoverflow.txt","w")
html_parser= HTMLParser.HTMLParser()
so = stackexchange.Site(stackexchange.StackOverflow)
so.be_inclusive()

results=[]
d=defaultdict()
i=0
for question in so.questions(pagesize=10):		
	try:
		if(i>20):
			break
		q=str(question.title.lower())
		b=str(question.body.lower())
		_id=question.id
		#c=[]
		words=[]
		uW=[]
		bd=''
		z=str(html_parser.unescape(str(b.encode('utf-8'))))
		f=0
		while f<len(z):
			x=z.find("<p>", f)
			y=z.find("</p>",f)
			if x>=0 and y>=0:
				s1=[m.start() for m in re.finditer('<code>', z[x+3:y])]
				s2=[m.start() for m in re.finditer('</code>', z[x+3:y])]
				s3=[m.start() for m in re.finditer('<a h', z[x+3:y])]
				s4=[m.start() for m in re.finditer('</a>', z[x+3:y])]
				r=0
				while r<len(s1) and r<len(s2):
					z[x+3:y]=re.sub(z[s1[r]:s2[r]+7],'', z[x+3:y])
					r=r+1
				r=0
				while r<len(s3) and r<len(s4):
					z[x+3:y]=re.sub(z[s3[r]:s4[r]+4],'', z[x+3:y])
					r=r+1
				bd+=BeautifulSoup(str(z[x+3:y].encode('utf-8'))).get_text()+' '	
				f=y+4
			else:
				break
		
		words=re.sub('[!@%^&*()$:"?<>=~,;`{}|]',' ',str(q+' '+bd))   
		words=re.sub('\n',' ',words)
		words=re.sub('_','-',words)
		pattern = re.compile(r'(\s)\-+(\s)') # ' ---- ' -> ' '
		words = pattern.sub(r'\1', words)
		pattern = re.compile(r'\.+(\s)')
		words = pattern.sub(r'\1', words)
		pattern = re.compile(r'(\s)\.+(\s)')
		words = pattern.sub(r'\1', words)
		words = re.sub("'",'', words)
		words= re.sub("^\d+\s|\s\d+\s|\s\d+$", " ", words)# asbcd 111 sad
		words= re.sub(" # ",' ',words)
		#clean_text=filter(lambda w: not w in s,words.split())
		#uniqueWords=[]
		#for word in clean_text:
		#	if not (word,clean_text.count(word)) in uniqueWords:
		#		uniqueWords.append((word,clean_text.count(word)))
		
		d[_id]=words
		#results.append(d)
		print i+1,"Post Collected-",_id
		i=i+1
		
	except Exception,e:
		print "EXCEPTION: ",str(e)
		pass
	
fh.write(json.dumps(d))		
fh.close()

