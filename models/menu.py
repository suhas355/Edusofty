# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## Customize your APP title, subtitle and menus here
#########################################################################

response.logo = A(B('web',SPAN(2),'py'),XML('&trade;&nbsp;'),
                  _class="brand",_href="http://www.web2py.com/")
response.title = request.application.replace('_',' ').title()
response.subtitle = ''

## read more at http://dev.w3.org/html5/markup/meta.name.html
response.meta.author = 'Your Name <you@example.com>'
response.meta.keywords = 'web2py, python, framework'
response.meta.generator = 'Web2py Web Framework'

## your http://google.com/analytics id
response.google_analytics_id = None

#########################################################################
## this is the main application menu add/remove items as required
#########################################################################

response.menu = [
    (T('Home'), False, URL('custom', 'index'), [])
]

DEVELOPMENT_MENU = True

#########################################################################
## provide shortcuts for development. remove in production
#########################################################################

def _():
    # shortcuts
    app = request.application
    ctr = request.controller
    if auth.is_logged_in():
        response.menu+= [
        (T('Profile'), False, URL('custom','profile')),
        (T('Tests'), False, URL('custom','tests')),
        (T('Statistics'), False, URL('custom','stats')
        )]  
        if auth.user.is_stud == False:
            response.menu += [
            (T('Upload Test'),False,URL('custom','test'))
            ]
    # useful links to internal and external resources


if DEVELOPMENT_MENU: _()

if "auth" in locals(): auth.wikimenu()
