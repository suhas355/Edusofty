# -*- coding: utf-8 -*-
# try something like
def index(): return dict()

@auth.requires_login() 
def home():
    return dict(message='hello from internal home')

@auth.requires_login() 
def happy():
    return dict(message='hello from happy')

@auth.requires_login()
def profile():
    redirect(URL('default','user',args='profile'))
