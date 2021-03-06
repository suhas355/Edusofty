# -*- coding: utf-8 -*-

#########################################################################
## This scaffolding model makes your app work on Google App Engine too
## File is released under public domain and you can use without limitations
#########################################################################

## if SSL/HTTPS is properly configured and you want all HTTP requests to
## be redirected to HTTPS, uncomment the line below:
# request.requires_https()

db = DAL('sqlite://edudb.sqlite')

session.connect(request, response, db=db)
    ## or store session in Memcache, Redis, etc.
    ## from gluon.contrib.memdb import MEMDB
    ## from google.appengine.api.memcache import Client
    ## session.connect(request, response, db = MEMDB(Client()))

## by default give a view/generic.extension to all actions from localhost
## none otherwise. a pattern can be 'controller/function.extension'
response.generic_patterns = ['*'] if request.is_local else []

## (optional) optimize handling of static files
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'
## (optional) static assets folder versioning
# response.static_version = '0.0.0'
#########################################################################
## Here is sample code if you need for
## - email capabilities
## - authentication (registration, login, logout, ... )
## - authorization (role based authorization)
## - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
## - old style crud actions
## (more options discussed in gluon/tools.py)
#########################################################################

from gluon.tools import Auth, Service, PluginManager

auth = Auth(db)
service = Service()
plugins = PluginManager()

auth.settings.extra_fields['auth_user']= [
Field('is_stud','boolean',comment='Do not check this box if you are a teacher'),
Field('dob','date')
]


## create all tables needed by auth if not custom tables
auth.define_tables(username=True, signature=False)

## configure email
mail = auth.settings.mailer
mail.settings.server = 'smtp.gmail.com:25'
mail.settings.sender = 'ks.suhas355@gmail.com'
mail.settings.login = 'ks.suhas355:govinda355@'

## configure auth policy
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True

#to redirect after successfull login
auth.settings.login_next = URL('custom','index')

## if you need to use OpenID, Facebook, MySpace, Twitter, Linkedin, etc.
## register with janrain.com, write your domain:api_key in private/janrain.key
from gluon.contrib.login_methods.janrain_account import use_janrain
use_janrain(auth, filename='private/janrain.key')

#########################################################################
## Define your tables below (or better in another model file) for example
##
## >>> db.define_table('mytable',Field('myfield','string'))
##
## Fields can be 'string','text','password','integer','double','boolean'
##       'date','time','datetime','blob','upload', 'reference TABLENAME'
## There is an implicit 'id integer autoincrement' field
## Consult manual for more options, validators, etc.
##
## More API examples for controllers:
##
## >>> db.mytable.insert(myfield='value')
## >>> rows=db(db.mytable.myfield=='value').select(db.mytable.ALL)
## >>> for row in rows: print row.id, row.myfield
#########################################################################

## after defining tables, uncomment below to enable auditing
# auth.enable_record_versioning(db)

db.define_table('testmap',
	Field('uid',db.auth_user,notnull=True),
	Field('tname','string'),
	Field('score','integer',notnull=True,default=1),
	Field('negative','double',IS_FLOAT_IN_RANGE(0.0, 1.0)),
    Field('category','list:string',notnull=True),
    migrate=True
	)

db.testmap.category.requires=IS_IN_SET(('Aptitude','Verbal','OS','Database'))
db.define_table('question',
                Field('tid',db.testmap,notnull=True),
                Field('qno','integer',notnull=True),
                Field('ques','string'),
                Field('opt_a','string'),
                Field('opt_b','string'),
                Field('opt_c','string'),
                Field('opt_d','string'),
                Field('answer','string'),
                migrate=True,
                primarykey=['tid','qno']
                )

db.define_table('stat',
    Field('stud_id',db.auth_user, notnull=True),
    Field('tid',db.testmap, notnull=True),
    Field('score','double'),
    Field('maxscore','double'),
    Field('timestamp','datetime'),
    primarykey = ['stud_id','timestamp']
    )