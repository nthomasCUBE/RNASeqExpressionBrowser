import sys

tmp=sys.argv[1]

a="""#!/usr/bin/env python
import cgi
import cgitb
import sys
import numpy
import os
import os.path
import MySQLdb
import string
import random

##################

TEMP="XXTEMP"

##################

cgitb.enable()

form = cgi.FieldStorage()

TYPE=form.getvalue("type")
PROJECT=form.getvalue("project")

try:
	if(TYPE=="eigengenes"):
		fid=TEMP+"/EIGENGENES_test.pdf"
	elif(TYPE=="heatmap"):
                fid=TEMP+"/EIGENGENES_test_hm.pdf"
	elif(TYPE=="genegroup"):
                fid=TEMP+"/EIGENGENES_test_bx.pdf"
	elif(TYPE=="network"):
                fid=TEMP+"/NETWORK.pdf"
	elif(TYPE=="REPORT"):
		fid=TEMP+"/"+PROJECT+"_comment_BOX.pdf"
	print "Content-type: application/pdf\\n\\n"
	with open(fid, "r") as f:
	    print f.read()
except Exception:
	print "Content-type: text/html\\n"
	print "Unfortunately, download did not work"
"""

a=a.replace("XXTEMP",tmp)
print a

