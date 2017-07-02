a="""#!/usr/bin/env python
import cgi
import cgitb
import sys
import MySQLdb
import string

cgitb.enable()

print 'Content-disposition:attachment;filename=download.csv\\r\\n\\r'
#print 'Content-type: application/csv\\r\\n\\r'

form = cgi.FieldStorage()
search = form.getvalue('search')
search2 = form.getvalue('search2')
search3 = form.getvalue('search3')
search4 = form.getvalue('search4')

if(search==None):
	search=""
if(search2==None):
	search2=""
if(search3==None):
	search3=""
if(search4==None):
	search4=""



sql= "SHOW COLUMNS FROM fpkm_map;"
db = MySQLdb.connect("$mysql_host","$mysql_user","$mysql_password","$mysql_database")
cursor = db.cursor()
cursor.execute(sql)
elements=cursor.fetchall()
for x in range(0,len(elements)):
	if(x==1):
		print "description","\\t",
        print elements[x][0],"\\t",

print

DOM={}
cursor.execute("select distinct r.* from hrd_map r")
elements=cursor.fetchall()
for el_ in elements:
	DOM[el_[0]]=el_[1]
	

cursor.execute("select distinct r.* from fpkm_map r,download_map r2 WHERE r.transcript=r2.transcript")
elements=cursor.fetchall()
for el_ in elements:
	for x in range(0,len(el_)):
		if(x!=1):
			print el_[x],
		else:
			if(DOM.get(el_[0])!=None):
				print DOM[el_[0]],"\\t",
			else:
				print "NA","\\t",
			print el_[1],
		if(x<len(el_)):
			print "\\t",
	print
"""

import sys

dom_map=sys.argv[1]
fpkm_map=sys.argv[2]
hrd_map=sys.argv[3]
go_map=sys.argv[4]
download_map=sys.argv[5]
mysql_host=sys.argv[6]
mysql_user=sys.argv[7]
mysql_database=sys.argv[8]
mysql_password=""
if(len(sys.argv)>9):
	mysql_password=sys.argv[9]

a=a.replace("$mysql_host",mysql_host)
a=a.replace("$mysql_user",mysql_user)
a=a.replace("$mysql_password",mysql_password)
a=a.replace("$mysql_database",mysql_database)

a=a.replace("dom_map",dom_map)
a=a.replace("fpkm_map",fpkm_map)
a=a.replace("hrd_map",hrd_map)
a=a.replace("go_map",go_map)
a=a.replace("download_map",download_map)

print a
