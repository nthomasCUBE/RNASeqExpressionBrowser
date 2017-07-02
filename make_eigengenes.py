import sys

host=sys.argv[1]
user=sys.argv[2]
password=sys.argv[3]
project=sys.argv[4]
database=sys.argv[5]
css=sys.argv[6]
tmp_dir=sys.argv[7]

template="""#!/usr/bin/env python
import os
import cgi
import cgitb
import sys
import MySQLdb
import string

cgitb.enable()

project_name="XXPROJECT"

print 'Content-type: text/html\\r\\n\\r'
print "<link rel='stylesheet' type='text/css' href='XXCSS'/>"

form = cgi.FieldStorage()

goids=form.getvalue("tx")

print "<div class='header'>"
print "<h1><a href='index.cgi'>"+project_name+"</a></h1>"
print "</div>"

db = MySQLdb.connect("XXHOST","XXUSER","XXPASSWORD","XXDATABASE")
fw=file("XXTMP_DIR/EIGENGENES_INPUT","w")
cursor=db.cursor()
cursor.execute("select column_name from information_schema.columns where table_name='"+project_name+"';")
elements=cursor.fetchall()

c_entry=[]
c_entry.append(elements[0][0])
for x in range(2,len(elements),3):
	c_entry.append(elements[x][0])
fw.write(string.join(c_entry,"\t")+"\\n")
	
cursor = db.cursor()
cursor.execute("select distinct r.* from test4."+project_name+" r,test4."+project_name+"DOWNLOAD r2 WHERE r.transcript=r2.transcript")
elements=cursor.fetchall()
i=0
for el_ in elements:
	c_entry=[]
	c_entry.append(str(el_[0]))
	for x in range(2,len(el_),3):
		c_entry.append(str(el_[x]))
	fw.write(string.join(c_entry,"\t")+"\\n")
fw.close()


fw=file("XXTMP_DIR/EIGENGENES_INPUT2","w")
cursor=db.cursor()
cursor.execute("select module,COUNT(DISTINCT A.transcript) from "+project_name+"DOWNLOAD A,"+project_name+"MODULE B WHERE A.transcript=B.transcript GROUP BY module;")
elements=cursor.fetchall()

for el_ in elements:
	fw.write(str(el_[0])+"\t"+str(el_[1])+"\\n")
fw.close()

os.system("R -f eigengenes.R > /dev/null")
os.system("R -f gene_net.R > /dev/null")

print "<hr>"

print "<h1>Eigengenes</h1>"
print "<a href='#eigengene'></a>"
print "<h2>Representative expression over all gene candidates</h2>"
print "<a href='export_file.cgi?type=eigengenes'>Eigengenes plot</a>"
print "</br>"

print "<hr>"

print "<h1>Heatmap</h1>"
print "<a href='#heatmap'></a>"
print "<h2>Depicting the expression of all gene candidates</h2>"
print "<a href='export_file.cgi?type=heatmap'>Heatmap of selected genes</a>"
print "</br>"

print "<hr>"

print "<h1>Gene-to-group information</h1>"
print "<a href='#group'></a>"
print "<h2>Grouping to genes to their gene-groups</h2>"
print "<a href='export_file.cgi?type=genegroup'>Gene distribution</a>"

print "<hr>"

print "<h1>Gene Network</h1>"
print "<a href='#network'></a>"
print "<h2>GeneNet</h2>"
print "<a href='export_file.cgi?type=network'>Gene Net</a>"

print "<hr>"

a=\"\"\"
<div class="footer">
<p>This web site was created with <a href="redir.aspx?C=Eo2--7tDUkyue5TkFWj3WEwCNpMPKdFItGWdZwPt1rsUueWFKeH_bk-f2wMC8NX_WJs7ni0Fkug.&amp;URL=http%3a%2f%2fmips.helmholtz-muenchen.de%2fplant%2fRNASeqExpressionBrowser%2findex.jsp" target="_blank">
RNAExpressionBrowser</a> </p>
</div>
"\"\"
print a
"""

template=template.replace("XXPROJECT",project)
template=template.replace("XXUSER",user)
template=template.replace("XXPASSWORD",password)
template=template.replace("XXHOST",host)
template=template.replace("XXDATABASE",database)
template=template.replace("XXCSS",css)
template=template.replace("XXTMP_DIR",tmp_dir)
print template


