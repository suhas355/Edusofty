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

@auth.requires_login() 
def upload():
	print request.vars.csvfile
	print "bla"
	if request.vars.csvfile != None:
		import_csv('db.test',request.vars.csvfile.file)
		response.flash = T('data uploaded')
	return dict() 

