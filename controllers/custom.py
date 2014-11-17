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
	return flist

def insertTest(t_name,cat,marks,negmarks,csvlist):
	try:
		t_id=db.testmap.insert(uid=auth.user.id,tname=t_name,score=marks,negative=negmarks,category=cat)
		db.commit()
	except:
		return False
	q_no=1
	print "-----------------------------"
	for line in csvlist:
		print q_no
		print t_id
		print q_no
		print line[0]
		print line[1]
		print line[2]
		print line[3]
		print line[4]
		print line[5]

		db.question.insert(tid=t_id,qno=q_no,ques=line[0],opt_a=line[1],opt_b=line[2],opt_c=line[3],opt_d=line[4],answer=line[5])
		print line
		q_no=q_no+1		
	return True
		


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

