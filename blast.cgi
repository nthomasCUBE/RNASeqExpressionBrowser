import sys

css_path=sys.argv[1]
db_path=sys.argv[2]
project=sys.argv[3]
blast_path=""
if(len(sys.argv)>4):
	blast_path=sys.argv[4]+"/"

a="""#!/usr/bin/env python
import cgi
import os
import cgitb
import sys
import MySQLdb
import string

cgitb.enable()

print 'Content-type: text/html\\r\\n\\r'
print "<link rel=\\"stylesheet\\" type=\\"text/css\\" href=\\"$css_path\\">"
print "<div class=\\"header\\">"
print "<h1><a href=\\"index.cgi\\">$project</a></h1>"
print "</div>"
print "<table>"
print "<tbody>"
print "<tr style=\\"text-align: center;\\">"
print "<td class=\\"headerinact\\" style=\\"width: 100%;\\">&nbsp;</td>"
print "<td id=\\"headerseq\\" class=\\"headerinact\\" style=\\"min-width: 160px;\\"><a class=\\"anone\\" target=\\"_blank\\" href=\\"./help.cgi\\">Help</a></td>"
print "</tr>"
print "</tbody>"
print "</table>"
print "<title>Blast results</title>"

form = cgi.FieldStorage()
fasta = form.getvalue('fasta')
eval=form.getvalue('eval')
prgm=form.getvalue('program')

if(fasta!=None):
	fw=file("XXX","w")
	fw.write(fasta)
	fw.close()

	if(prgm=="BLASTN"):
		cmd=("$blast_pathblastn -query XXX -db transcripts_NT.fa -evalue "+str(eval)+" -outfmt 10 > YYY")
	else:
                cmd=("$blast_pathblastp -query XXX -db transcripts_AA.fa -evalue "+str(eval)+" -outfmt 10 > YYY")

	os.system(cmd)

	if(os.stat("YYY")[6]!=0):
		fh=file("YYY")
		print "</br></br>"
		print "<center>"
		print "<table border='1' width='80%'>"
		print "<tr><td><b>Query</b></td><td><b>Expression</b></td><td><b>Gene match</b></td><td><b>identity</b></td><td><b>bp length</b></td><td><b>score</b></td></tr>"
		for line in fh.readlines():
			line=line.strip()
		 	vals=line.split(",")
			print "<tr>",
			print "<td>"+vals[0]+"</td>"+"<td><a href='gene_report.cgi?gene="+vals[1]+"'>Expression</a></td>"+"<td>"+str(vals[1])+"</td>"+"<td>"+vals[2]+"</td>"+"<td>"+vals[3]+"</td>"+"<td>"+vals[11]+"</td>";
			print "</tr>"
		print "</table>"
		print "</center>"
	else:
		print "<center><h1>Unfortunately no matches were found when sequences were compared against project related sequences</h1></center>"
		print "<center><h1><a href='index.cgi'>Return to Main page</a></h1>"
else:
	print "<center><h1>Unfortunately no matches were found when sequences were compared against project related sequences</h1></center>"
	print "<center><h1><a href='index.cgi#Blast'>Return to Main page</a></h1>"

print "</br>"
print "<div class=\\"footer\\">"
print "<p>"
print "This web site was created with <a href=\\"http://mips.helmholtz-muenchen.de/plant/RNASeqExpressionBrowser/index.jsp\\" target=\\"_blank\\">RNAExpressionBrowser</a>"
print "</p>"
print "</div>"

"""

a=a.replace("$css_path",css_path)
a=a.replace("$blast_path",blast_path)
a=a.replace("$project",project)
a=a.replace("$db_path",db_path)

print a

