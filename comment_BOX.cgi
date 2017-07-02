#!/usr/bin/env python
import cgi
import cgitb
import MySQLdb
import os

PROJECT="__PROJECT__"

cgitb.enable()

print 'Content-type: text/html\r\n\r'

a="""\documentclass[11pt]{article}

\usepackage[margin=1in]{geometry} % Required to make the margins smaller to fit more content on each page
\usepackage[linkcolor=blue]{hyperref} % Required to create hyperlinks to questions from elsewhere in the document
\hypersetup{pdfborder={0 0 0}, colorlinks=true, urlcolor=blue} % Specify a color for hyperlinks
\usepackage{microtype} % Slightly tweak font spacing for aesthetics
\usepackage{palatino} % Use the Palatino font

\\begin{document}

\section{Comments}

"""
A=a

sql= "SELECT * FROM "+PROJECT+"COMMENTS;"
try:
	db = MySQLdb.connect("__HOST__","__USER__","__PASSWORD__","__DB__")
	cursor = db.cursor()
except Exception:
	print "Database connection failed"
	pass

cursor.execute(sql)
elements=cursor.fetchall()
for el_ in elements:
	_e=el_[0].replace("_","\_")
	_v=el_[1].replace("_","\_")
	_e=_e.replace("%","\%")
	_v=_v.replace("%","\%")
       	A=A+"\subsection{"+_e+"}""\n"
	A=A+_v+"\n"

A=A+"\section{Modules}"

sql="SELECT * from "+PROJECT+"MODULE ORDER BY module ASC;"
cursor = db.cursor()
cursor.execute(sql)
elements=cursor.fetchall()
mm={}
for el_ in elements:
        E1=el_[0].replace("_","\_")
	E2=el_[1].replace("_","\_")

	if(mm.get(E2)==None):
		mm[E2]={}
	mm[E2][E1]=1

cmd="\\begin{table}[!ht]\\tiny"
cmd=cmd+"\n"+"\\begin{tabular}{|c|c|}"
mk=mm.keys()
mk.sort()
cmd=cmd+"\n"+"\\hline"
cmd=cmd+"\n"+"Module"+" & "+"Number of genes"+"\\\\"
cmd=cmd+"\n"+"\\hline"
cs=0
for mm_ in mk:
	cmd=cmd+"\n"+str(mm_)+" &  "+str(len(mm[mm_].keys()))+"\\\\"
	cs=cs+len(mm[mm_].keys())
cmd=cmd+"\n"+"\\hline"
cmd=cmd+"\n"+"Total"+" & "+str(cs)+"\\\\"
cmd=cmd+"\n"+"\\hline"
cmd=cmd+"\n"+"\end{tabular}"
cmd=cmd+"\n"+"\end{table}"
A=A+cmd
A=A+"\n"+"\end{document}"

fw=file("__TEMP__/"+PROJECT+"_comment_BOX.tex","w")
fw.write(A)
fw.close()

os.system("cd __TEMP__/;pdflatex "+PROJECT+"_comment_BOX.tex > /dev/null")

print "<h1>Project-related comments...</h1>"
print "<html>"
print "<a href='./export_file.cgi?type=REPORT;project="+PROJECT+"'>"+"Comments included so far"+"</a>"
print "</html>"
