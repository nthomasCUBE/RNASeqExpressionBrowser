a="""#!/usr/bin/env python
import cgi
import cgitb
import sys
import MySQLdb
import string

cgitb.enable()

print 'Content-type: text/html\\r\\n\\r'

form = cgi.FieldStorage()
goids = form.getvalue('goids')
if(goids!=None):
	goids=goids.strip()
	goids=goids.split()
	goids=string.join(goids,",")
else:
	goids=""

print "<html>" 
print "<head>" 
print "<meta http-equiv=\\"refresh\\" content=\\"0;url=search.cgi?search="+goids+"\\"/>"
print "<title>You are going to be redirected</title>"
print "</head>" 
print "<body>"
print "Redirecting"
print "</body>"
print "</html>"

"""

print a
