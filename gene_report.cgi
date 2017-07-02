import string
import sys

# ------------------------------------------------------------------------------------------
labels=sys.argv[1]
labelsA=labels.split(",")
fpkm_map=sys.argv[2]
dom_map=sys.argv[3]
hrd_map=sys.argv[4]
cmt_map=sys.argv[5]
seq_nt_map=sys.argv[6]
seq_aa_map=sys.argv[7]
db_link_path=sys.argv[8]
css_path=sys.argv[9]
mysql_host=sys.argv[10]
mysql_user=sys.argv[11]
project=sys.argv[12]
mysql_database=sys.argv[13]
mysql_password=""
if(len(sys.argv)>14):
	mysql_password=sys.argv[14]
# ------------------------------------------------------------------------------------------

def print_content(a):
	s=a.replace("$project",project)
	s=s.replace("$fpkm_map",fpkm_map)
        s=s.replace("$dom_map",dom_map)
	s=s.replace("$cmt_map",cmt_map)
        s=s.replace("$hrd_map",hrd_map)
        s=s.replace("$css_path",css_path)
	s=s.replace("$db_link_path",db_link_path)
	s=s.replace("$seq_nt_map",seq_nt_map)
	s=s.replace("$seq_aa_map",seq_aa_map)
	s=s.replace("$labels",labels)
        print s

a="""#!/usr/bin/env python
import cgi
import cgitb
import sys
import MySQLdb
import string

cgitb.enable()

print 'Content-type: text/html\\r\\n\\r'

form = cgi.FieldStorage()
gene = form.getvalue('gene')
save=form.getvalue('save')

a=\"\"\"<html>

<head>
\"\"\"
print a
if(save!=None):
	tx=form.getvalue('tx')
"""
print a
print "\tdb = MySQLdb.connect('"+mysql_host+"','"+mysql_user+"','"+mysql_password+"','"+mysql_database+"')"
print "\tcursor = db.cursor()"
print "\tcursor.execute(\"DELETE FROM "+cmt_map+" WHERE transcript=%s;\",[gene]);"
print "\tcursor.execute(\"INSERT INTO "+cmt_map+" VALUES (%s,%s);\",[gene,tx.strip()]);"
a="""
print "<title>Gene report: "+str(gene)+"</title>"
a=\"\"\"</head>
<body>
<div class="header">
<h1><a href="index.cgi">$project</a></h1>
</div> 
<table>
<tbody>
<tr style="text-align: center;">
<td class="headerinact" style="width: 100%;">&nbsp;</td>
<td id="headerseq" class="headerinact" style="min-width: 160px;"><a class="anone" target="_blank" href="./help.cgi">Help</a></td>
</tr>
</tbody>
</table>
<script type='text/javascript' src='https://www.google.com/jsapi'></script>
<script type='text/javascript'>
google.load('visualization', '1', {packages:['table','corechart']});
google.setOnLoadCallback(drawChart);

function drawChart() {

var data1 = new google.visualization.DataTable();
data1.addColumn('string', 'Condition');
data1.addColumn('number', 'Expression');

var options = {
title: 'Expression per condition',
vAxis: {title: 'Expression strength',  titleTextStyle: {color: 'grey'}},
legend: {position: 'none'},tooltip:{trigger:'none'},enableInteractivity: false

};
\"\"\"
print a
"""
print_content(a)
print "db = MySQLdb.connect('"+mysql_host+"','"+mysql_user+"','"+mysql_password+"','"+mysql_database+"')"







a="""
cursor = db.cursor()
cursor.execute("SELECT * FROM $fpkm_map WHERE transcript=%s;",[gene]);
elements=cursor.fetchall()
match_found=False
for el_ in elements:
	if(gene==el_[0]):
		labelsA="$labels".split(",")
		cmd=[]
		cmd.append("['A','','','','']")
		for x in range(2,len(el_),3):
			print "data1.addRow(['"+labelsA[(x-2)/3+2]+"',"+str(el_[x])+"])";
			cmd.append("['"+labelsA[(x-2)/3+2]+"',"+str(el_[x+1])+","+str(el_[x])+","+str(el_[x])+","+str(el_[x+2])+"]")
		print "var data = google.visualization.arrayToDataTable(["+string.join(cmd,",")+"]);"	
		match_found=True

a=\"\"\"
var table1 = new google.visualization.Table(document.getElementById('table_div'));
table1.draw(data1, {showRowNumber: true});
var data2 = new google.visualization.DataTable();
data2.addColumn('string', 'Transcript');
data2.addColumn('string', 'Domain information');
\"\"\"
print a
"""
print_content(a)













print "db = MySQLdb.connect('"+mysql_host+"','"+mysql_user+"','"+mysql_password+"','"+mysql_database+"')"
a="""
cursor = db.cursor()
cursor.execute("select distinct transcript,domain from $dom_map WHERE domain NOT LIKE '%GO%';")
elements=cursor.fetchall()
for el_ in elements:
	if(gene==el_[0]):
		cmd="data2.addRow(['"+el_[0]+"','"+str(el_[1])+"'])";
		print cmd


a=\"\"\"
var table2 = new google.visualization.Table(document.getElementById('domain_div'));
table2.draw(data2, {showRowNumber: true});
var data3 = new google.visualization.DataTable();
data3.addColumn('string', 'Transcript');
data3.addColumn('string', 'GO term');
\"\"\"
print a
"""
print_content(a)












print "db = MySQLdb.connect('"+mysql_host+"','"+mysql_user+"','"+mysql_password+"','"+mysql_database+"')"
a="""
cursor = db.cursor()
cursor.execute("select distinct transcript,domain from $dom_map WHERE domain LIKE '%GO%';");
elements=cursor.fetchall()
for el_ in elements:
        if(gene==el_[0]):
                cmd="data3.addRow(['"+el_[0]+"','"+str(el_[1])+"'])";
                print cmd
a=\"\"\"
var table3 = new google.visualization.Table(document.getElementById('go_div'));
table3.draw(data3, {showRowNumber: true});
var chart = new google.visualization.CandlestickChart(document.getElementById('chart_exp'));
chart.draw(data, options);
}

</script>
<link rel="stylesheet" type="text/css" href="$css_path">
<br/>
<br/>

\"\"\"
print a

cursor = db.cursor()
cursor.execute("select distinct transcript,description from $hrd_map;")
elements=cursor.fetchall()
for el_ in elements:
        if(gene==el_[0]):
		print "<h1>",el_[0],"</h1>"
		print "<p>",el_[1],"</p>"


print "<h2>Expression profile</h2>"
print "<p><div id='chart_exp' style='max-width: 1000px;'></div></p>"
if(match_found==False):
        print "<font size='3' color='red'><h1>There is no expression information available for this gene</h1></font>"
a=\"\"\"
<div id='table_div'  style="width: 500px;"></div>
<h2>External annotation</h2>
<h3>Domains</h3><div id='domain_div' style="width: 500px;"></div></p>
<h3>Gene Ontology</h3><div id='go_div' style="width: 500px;"></div></p>

<h2>Comment-Box</h2>
\"\"\"
print a





cursor = db.cursor()
cursor.execute("SELECT comments FROM $cmt_map WHERE transcript=%s;",[gene]);
elements=cursor.fetchall()
print "<form id=\\"comment\\" name=\\"comment\\" method=\\"post\\" action=\\"gene_report.cgi?save=1;gene="+gene+"\\">"
a=\"\"\"
<form id="comment" name="comment" method="post" action="gene_report.cgi?save=1">
<textarea name="tx" id="tx" style="resize:none" rows="6" cols="80" id="goids" name="goids" value="goids">\"\"\"
print a
for el_ in elements:
	print el_[0],

print "</textarea>"
print "<input type='reset' value='Reset'>"
print "<input type='submit' value='Submit'>"
print "</form>"

a=\"\"\"


<h2>Links to external data</h2>
<li><a href='$db_link_path



\"\"\"


print "<h2>Sequences (Nucleotides)</h2>"
cursor = db.cursor()
cursor.execute("SELECT transcript,sequence FROM $seq_nt_map WHERE transcript LIKE %s or transcript=%s;",["%"+gene+".%",gene]);
elements=cursor.fetchall()
print "<textarea rows='6' cols='80'>"
for e in elements:
        print ">"+str(e[0])+'\\n'+str(e[1])
print "</textarea>"
print "<h2>Sequences (Amino acids)</h2>"
cursor = db.cursor()
cursor.execute("SELECT transcript,sequence FROM $seq_aa_map WHERE transcript LIKE %s or transcript=%s;",["%"+gene+".%",gene]);
elements=cursor.fetchall()
print "<textarea rows='6' cols='80'>"
for e in elements:
	print ">"+str(e[0])+'\\n'+str(e[1])
print "</textarea>"
print "<title>Gene report: "+str(gene)+"</title>"
print a+str(gene)+"'>"
a=\"\"\"Link to database</a></li>
</body>
</br>

        <div class="footer">
                <p>
                        This web site was created with <a
                                href="http://mips.helmholtz-muenchen.de/plant/RNASeqExpressionBrowser/index.jsp"
                                target="_blank">RNAExpressionBrowser</a>
                </p>
        </div>

</html>
\"\"\"
print a









"""
print_content(a)

