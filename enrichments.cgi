#!/usr/bin/env python
import cgi
import cgitb
import sys
import numpy
import os
import os.path
import MySQLdb
import string
import random

cgitb.enable()

form = cgi.FieldStorage()
ID=form.getvalue("ID")
opt=form.getvalue("opt")

a="""
<!DOCTYPE html>
<link rel="stylesheet" type="text/css" href="http://seacow.helmholtz-muenchen.de//main.css">
<div class='header'>
<h1><a href='index.cgi'>dattel</a></h1>
</div>

<script type="text/javascript">
function formType(value){
	window.location="enrichments.cgi?opt="+value;
}
</script>

<html>
<h1>Gene enrichment analysis</h1>
<p>
Gene enrichment were performed for both, the differentially expressed gene sets and well as
by considering the co-expressed network modules. The enrichment of terms was calculated
with the tool GOStats.
</p>
__OPT__
__BF__
__MF__
<br>
<p>
<h2>Links of interest</h2>
<a href="http://revigo.irb.hr/">Link to REVIGO allows to visualize enriched GO terms</a>
</p>
<br>
<div class="footer">
<p>This web site was created with <a href="redir.aspx?C=Eo2--7tDUkyue5TkFWj3WEwCNpMPKdFItGWdZwPt1rsUueWFKeH_bk-f2wMC8NX_WJs7ni0Fkug.&amp;URL=http%3a%2f%2fmips.helmholtz-muenchen.de%2fplant%2fRNASeqExpressionBrowser%2findex.jsp" target="_blank">
RNAExpressionBrowser</a> </p>
</div>
</html>
"""

files=os.listdir("enrichment")
OPT={}
for f_ in files:
	if(f_.find("BF.TXT")!=-1):
		OPT[f_.split(".")[0]]=1
	elif(f_.find("MF.TXT")!=-1):
		OPT[f_.split(".")[0]]=1

if(opt==None):
	if(len(OPT.keys())>0):
		opt=OPT.keys()[0]


OK=OPT.keys()
if(len(OK)>0):
	OK.sort()

cmdO="<select onchange=\"formType(this.value);\">"
if(opt!=None):
	cmdO=cmdO+"<option>"+opt+"</option>"
for OPT_ in OK:
	if(opt!=OPT_):
		cmdO=cmdO+"<option>"+OPT_+"</option>"
cmdO=cmdO+"</select>"
a=a.replace("__OPT__",cmdO)

files=os.listdir("enrichment")
cmdA=""

if(opt!=None):
	cmd=[]
	cmd.append("<h2><b>Biological Functions</b></h2>")
	cmd.append("<table border='1'>")
	cmd.append("<tr><td>module</td><td>GO id</td><td>P-value</td><td>Genes in Module</td><td>Genes total</td><td>description</td><td>Links</td></tr>")
	fh=file("enrichment/"+opt+".BF.TXT")
	for line in fh.readlines()[1:]:
		line=line.strip()
		line=line.replace("\"","")
		vals=line.split("\t")
		ee=[opt.split(".")[0],vals[1],vals[2],vals[5],vals[6],vals[len(vals)-1],"<a href='search.cgi?search3="+vals[1]+"&search4=&comment=&module="+opt.split(".")[0]+"&module2=---&sql='>Show Genes</a>"]
		ee="<tr><td>"+string.join(ee,"</td><td>")+"</td></tr>"
		cmd.append(ee)
	cmd.append("</table>")	
	cmdA=cmdA+string.join(cmd,"\n")
a=a.replace("__BF__",cmdA)

files=os.listdir("enrichment")
cmdA=""

if(opt!=None):
        cmd=[]
        cmd.append("<h2><b>Molecular Functions</b></h2>")
        cmd.append("<table border='1'>")
        cmd.append("<tr><td>module</td><td>GO id</td><td>P-value</td><td>Genes in Module</td><td>Genes total</td><td>description</td><td>Links</td></tr>")
	fh=file("enrichment/"+opt+".MF.TXT")
	for line in fh.readlines()[1:]:
		line=line.strip()
		line=line.replace("\"","")
		vals=line.split("\t")
 		ee=[opt.split(".")[0],vals[1],vals[2],vals[5],vals[6],vals[len(vals)-1],"<a href='search.cgi?search3="+vals[1]+"&search4=&comment=&module="+opt.split(".")[0]+"&module2=---&sql='>Show Genes</a>"]
		ee="<tr><td>"+string.join(ee,"</td><td>")+"</td></tr>"
		cmd.append(ee)
	cmd.append("</table>")
	cmdA=cmdA+string.join(cmd,"\n")
a=a.replace("__MF__",cmdA)



print a


