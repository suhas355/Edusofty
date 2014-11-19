# -*- coding: utf-8 -*-
# try something like
def index(): return dict()

@auth.requires_login() 
def home():
    return dict(message='hello from internal home')

@auth.requires_login()
def profile():	
    redirect(URL('default','user',args='profile'))

@auth.requires_login() 
def import_csv(table, file):
    re=db.test.import_from_csv_file(file)
    print re

def validate(csvfile):
	import csv
	csvlist = csvfile.value.split('\n')
	tcsv = csv.reader(csvlist,skipinitialspace=True)
	flist = []

	for i in tcsv:
		if len(i) != 6:
			return False
		if i[5] not in ['A','B','C','D']:
			return False

		flist.append(i)
	if len(flist) < 10 :
		return False
	return flist

def insertTest(t_name,cat,marks,negmarks,csvlist):
	try:
		t_id=db.testmap.insert(uid=auth.user.id,tname=t_name,score=marks,negative=negmarks,category=cat)
		db.commit()
	except:
		return False
	q_no=1
	for line in csvlist:
		db.question.insert(tid=t_id,qno=q_no,ques=line[0],opt_a=line[1],opt_b=line[2],opt_c=line[3],opt_d=line[4],answer=line[5])
		q_no=q_no+1		
	return True
	
@auth.requires_login()	
def stats():
	if auth.user.is_stud==True:
		tname=[]
		percent = []
		rows = db(db.stat.stud_id==auth.user.id).select()
		for row in rows:
			per=(row.score / row.maxscore * 100 )
			percent.append(per)
			tnameTuple=db(db.testmap.id==row.tid).select(db.testmap.tname).first()
			tname.append(tnameTuple['tname'])
		
		return dict(tlist = tname,scount = percent,xvalue='tests taken',yvalue='percentage',unit='score in %')
	else:
		tname =[]
		stud_taken=[]
		rows = db(db.testmap.uid==auth.user.id).select(db.testmap.id,db.testmap.tname)
		for row in rows:
			tname.append(row.tname)
			studs = db(db.stat.tid==row.id).count()
			stud_taken.append(studs)

		return dict(tlist = tname,scount = stud_taken,xvalue='tests uploaded',yvalue='No of students taken',unit='No of students')

@auth.requires_login() 
def upload():
	if request.vars.csvfile != None:
		ret = validate(request.vars.csvfile)
		if not ret:
			response.flash=T('Error in file.')
			return dict()
		
		status=insertTest(request.vars.tname,request.vars.cat,request.vars.marks,request.vars.negmarks,ret)
		if status == False:
			response.flash=T('Error in upload')
			return dict()

		#import_csv('db.test',request.vars.csvfile.file)
		response.flash = T('data uploaded')
	return dict() 

@auth.requires_login() 
def dispList():	
	ids=[]
	names=[]
	cat=request.vars['cat']
	if not request.vars['ids'] is None:
		ids.append(request.vars['ids'])
		names.append(request.vars['names'])
	else:
		return dict(ids=None,names=None,cat=cat)	
	return dict(ids=ids,names=names,cat=cat)

@auth.requires_login() 
def testlist():
	return dict()

@auth.requires_login() 
def showTestList():
	response.flash = T('click is on')
	namelist=[]
	idlist=[]
	for row in db(db.testmap.category==request.args[0]).select():
		idlist.append(row.id)
		namelist.append(row.tname)
	redirect(URL('custom','dispList',vars=dict(ids=idlist,names=namelist,cat=request.args[0])))

@auth.requires_login() 
def testpage():
	#print request.args
	row=db(db.testmap.id==request.args[0]).select().first()
	return dict(tid=row.id,marks=row.score,negmarks=row.negative)

def getRandomList():
	qlist=[]


@auth.requires_login() 
def testStart():
	rows=db(db.question.tid==request.args[0]).select()
	tnamerow=db(db.testmap.id==request.args[0]).select(db.testmap.tname).first()
	tname=tnamerow['tname']
	ques=[]
	for row in rows:
		ques.append([row.qno,row.ques,row.opt_a,row.opt_b,row.opt_c,row.opt_d,row.answer])

	qcount = len(ques)
	maxques = min(10,qcount)
	if qcount == maxques:
		return dict(tid=request.args[0],ques=ques,tname=tname)
	qlist=[]
	qno =[]
	from random import randint
	while len(qno) != maxques:
		num = randint(1,qcount-1)
		present = True if num in qno else False
		if present == False:
			qlist.append(ques[num])
			qno.append(num)
	
	return dict(tid=request.args[0],ques=qlist,tname=tname)

@auth.requires_login() 
def evaluate():	
	tid=request.args[0]
	marks=db(db.testmap.id==tid).select().first()
	pos=marks.score
	neg=marks.negative
	score=0
	tname=db(db.testmap.id==tid).select(db.testmap.tname).first()
	for qno in request.vars:
		if qno == 'submit':
			continue
		ans=db((db.question.tid==tid) & (db.question.qno==qno)).select(db.question.answer).first()

		if ans['answer']==request.vars[qno]:
			score=score+pos
		else:
			score=score-neg

	#Insert obtained score in stat table
	maxscore = pos*10
	import sqlite3
	from datetime import datetime
	now = datetime.now()
	db.stat.insert(stud_id=auth.user.id,tid = tid,score=score,maxscore=maxscore,timestamp=now)
	return dict(score=score,perques=pos,tname= tname['tname'])
