import string
import sys

# ------------------------------------------------------------------------------------------

labels=sys.argv[1]
fpkm_map=sys.argv[2]
hrd_map=sys.argv[3]
dom_map=sys.argv[4]
go_map=sys.argv[5]
module=sys.argv[6]
css_path=sys.argv[7]
filter1=sys.argv[8]
filter2=sys.argv[9]
filter3=sys.argv[10]
filter4=sys.argv[11]
filter5=sys.argv[12]
filter6=sys.argv[13]
filter7=sys.argv[14]
filter8=sys.argv[15]
filter9=sys.argv[16]
filter10=sys.argv[17]
mysql_host=sys.argv[18]
mysql_user=sys.argv[19]
project=sys.argv[20]
mysql_database=sys.argv[21]
mysql_password=""
if(len(sys.argv)>22):
	mysql_password=sys.argv[22]
module_map=project+"MODULE"
cmt_map=project+"COMMENTS"
deg_map=project+"DEG"
download_map=project+"DOWNLOAD"
promoter_map=project+"PROMOTER"
# ------------------------------------------------------------------------------------------

def print_content(a):
	a=a.replace("$project",project)
	t=string.Template(a)
	s=t.substitute(locals())
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
search = form.getvalue('search')
search2 = form.getvalue('search2')
search3 = form.getvalue('search3')
search4 = form.getvalue('search4')
comment = form.getvalue('comment')
sql=form.getvalue('sql')

module=form.getvalue('module')
module2=form.getvalue('module2')
promoter=form.getvalue('promoter')
hub=form.getvalue('hub')

if(module==None):
        module="---"
if(module2==None):
	module2="---"
if(promoter==None):
	promoter="---"

deg=module2

x1=search
x2=search2
x3=search3
x4=search4

if(x1==None):
        x1="---"
if(x2==None):
        x2="---"
else:
	x2=str(x2)
if(x3==None):
        x3="---"
else:
	x3=x3.split()[0]
if(x4==None):
        x4="---"
if(comment==None):
	comment="---"
a=\"\"\"<html>
<head>
<title>RNASeqExpressionBrowser</title>
<div class="header">
<h1><a href="index.cgi">$project</a></h1>
</div> 
<div id="content-menu">
<table>
<tbody>
<tr style="text-align: center;">
<td id="headerkey" class="headeract" style="min-width: 160px;">
\"\"\"
print a
print "<a class=\\"anone\\" href=\\"export.cgi?search="+x1+"&search2="+x2+"&search3="+x3+"&search4="+x4+"\\">Download</a>"
print "<td id='headerkey' class='headeract' style='min-width: 160px;'>"
print "<a class=\\"anone\\" href=\\"eigengenes.cgi\\">Eigen-Genes</a>"
print "<td id='headerkey' class='headeract' style='min-width: 160px;'>"
print "<a class=\\"anone\\" href=\\"eigengenes.cgi\\">Heat-Maps</a>"
print "<td id='headerkey' class='headeract' style='min-width: 160px;'>"
print "<a class=\\"anone\\" href=\\"eigengenes.cgi\\">Gene-Groups</a>"
print "<td id='headerkey' class='headeract' style='min-width: 160px;'>"
print "<a class=\\"anone\\" href=\\"eigengenes.cgi\\">Gene-Network</a>"
a=\"\"\"<td class="headerinact" style="width: 100%;">&nbsp;</td>
<td id="headerseq" class="headerinact" style="min-width: 160px;"><a class="anone" target="_blank" href="./help.cgi">Help</a></td>
</tr>
</tbody>
</table>
<div class="content-menu-help">Search Results</div>
</div>

<div class="content-menu-gradient">
<table>
<tr>
<td style="margin: 0; padding: 0; border: 0;">Expression Gradient:</td>

<td style='width:100px;background:#D0D0D0;border-spacing:0px'>0&#37;</td>
<td style='width:100px;background:#ADD8E6;border-spacing:0px'>0-10&#37;</td>
<td style='width:100px;background:#13DBED;border-spacing:0px'>10-20&#37;</td>
<td style='width:100px;background:#13ED92;border-spacing:0px'>20-30&#37;</td>
<td style='width:100px;background:#13ED3F;border-spacing:0px'>30-40&#37;</td>
<td style='width:100px;background:#67ED13;border-spacing:0px'>40-50&#37;</td>
<td style='width:100px;background:#BEED13;border-spacing:0px'>50-60&#37;</td>
<td style='width:100px;background:#EDDB13;border-spacing:0px'>60-70&#37;</td>
<td style='width:100px;background:#ED9913;border-spacing:0px'>70-80&#37;</td>
<td style='width:100px;background:#ED6A13;border-spacing:0px'>80-90&#37;</td>
<td style='width:100px;background:#ED2C13;border-spacing:0px'>90-100&#37;</td>

</tr>
</table>
</div>
\"\"\"
print a
a=\"\"\"
<script type="text/javascript" src="https://www.google.com/jsapi"></script>
<script type="text/javascript">
google.load('visualization', '1.0', {'packages':['controls','table']});
google.setOnLoadCallback(drawVisualization);

var options = {'showRowNumber': true,'allowHtml':true};

function drawVisualization() {
  data = new google.visualization.DataTable();

"""
print_content(a)

labelsA=labels.split(",")

print "var nmb_L="+str(len(labelsA))+";"

for x in range(0,len(labelsA)):
	if(x>=2):
		print "data.addColumn('number','"+labelsA[x]+"');";
	else:
		if(x!=1):
	                print "data.addColumn('string','"+labelsA[x]+"');";
		else:
                        print "data.addColumn('string','description');";
                        print "data.addColumn('string','gene');";

a="""
\"\"\"
print a
db = MySQLdb.connect("$mysql_host","$mysql_user","$mysql_password","$mysql_database")
cursor = db.cursor()
unique_k={}
found_match=False

ALLOWED_GENES={}

cursor.execute("select r2.* from $hrd_map r2")
elements=cursor.fetchall()
DOM={}
for el_ in elements:
	if(len(el_[1])>50):
		DOM[el_[0]]=el_[1][0:50]+"..."
	else:
		DOM[el_[0]]=el_[1]
def add_header(cmd,el_):
	for x in range(0,2):
		if(x==0):
			cmd=cmd+\"\\"\"+str(el_[x])+\"\\"\"
		else:
			if(DOM.get(el_[0])!=None):
				cmd=cmd+\"\\"\"+str(DOM[el_[0]])+\"\\"\"
			else:
				cmd=cmd+\"\\"\"+"-"+\"\\"\"
		if(x!=(len(el_)-1)):
			cmd=cmd+","
	return cmd



ALLOWED_GENES={}

cmd_all=""
arr=[]

if(x1!="---"):
	x1=x1.split(",")
	for x1_ in x1:
	        if(len(cmd_all)>0):
	       	        cmd_all=cmd_all+" UNION ALL "
	        cmd_all=cmd_all+"select r1.transcript from $fpkm_map r1 WHERE r1.transcript=%s"
		arr.append(x1_)
if(x2!="---"):
	if(len(cmd_all)>0):
		cmd_all=cmd_all+" UNION ALL "
	cmd_all=cmd_all+"select r1.transcript FROM $hrd_map r1 WHERE r1.description LIKE %s"
	arr.append("%"+x2+"%")
if(x3!="---"):
	if(len(cmd_all)>0):
		cmd_all=cmd_all+" UNION ALL "
	cmd_all=cmd_all+"select r2.transcript FROM $dom_map r2, $go_map r1 WHERE r2.domain=r1.go_id AND r1.go_offspring LIKE %s"
	arr.append("%"+x3+";")
	cmd_all=cmd_all+" UNION ALL "
	cmd_all=cmd_all+"select r1.transcript FROM $dom_map r1 WHERE r1.domain=%s"
        arr.append(x3)
if(x4!="---"):
        if(len(cmd_all)>0):
                cmd_all=cmd_all+" UNION ALL "
        cmd_all=cmd_all+"select r1.transcript FROM $dom_map r1 WHERE r1.domain LIKE %s"
        arr.append(x4)
if(comment!="---"):
        if(len(cmd_all)>0):
                cmd_all=cmd_all+" UNION ALL "
        cmd_all=cmd_all+"select r1.transcript FROM $cmt_map r1 WHERE r1.comments LIKE %s"
        arr.append("%"+comment+"%")
if(len(arr)>0):
	cursor.execute(cmd_all,arr)
        elements=cursor.fetchall()
        for el_ in elements:
                ALLOWED_GENES[el_[0]]=1

has_deg=False
has_module=False
has_promoter=False

if(deg!="---"):
	has_deg=True
if(module!="---"):
	has_module=True
if(promoter!="---"):
	has_promoter=True

no_filter=False
if(has_deg==True and has_module==True and has_promoter==True):
	cmd="select r1.transcript from $deg_map r1, $module_map r2,$promoter_map r3 WHERE r1.transcript=r2.transcript and r1.transcript=r3.transcript and r1.comparison=%s and r2.module=%s and r3.promoter=%s"
        cursor.execute(cmd,[deg,module,promoter])
elif(has_deg==True and has_module==True):
	cmd="select r1.transcript from $deg_map r1,$module_map r2 WHERE r1.transcript=r2.transcript and r1.comparison=%s and r2.module=%s"
	cursor.execute(cmd,[deg,module])
elif(has_deg==True and has_promoter==True):
        cmd="select r1.transcript from $deg_map r1,$promoter_map r2 WHERE r1.transcript=r2.transcript and r1.comparison=%s and r2.promoter=%s"
        cursor.execute(cmd,[deg,promoter])
elif(has_promoter==True and has_module==True):
        cmd="select r1.transcript from $promoter_map r1,$module_map r2 WHERE r1.transcript=r2.transcript and r1.promoter=%s and r2.module=%s"
        cursor.execute(cmd,[promoter,module])
elif(has_promoter==True):
	cmd="select r1.transcript from $promoter_map r1 WHERE r1.promoter=%s "
        cursor.execute(cmd,[promoter])
elif(has_module==True):
        cmd="select r1.transcript from $module_map r1 WHERE r1.module=%s"      
        cursor.execute(cmd,[module])
elif(has_deg==True):
        cmd="select r1.transcript from $deg_map r1 WHERE r1.comparison=%s"
        cursor.execute(cmd,[deg])
else:
	no_filter=True

FILTERED_GENES={}	
if(no_filter==False):
        elements=cursor.fetchall()
        for el_ in elements:
		FILTERED_GENES[el_[0]]=1

if(len(ALLOWED_GENES.keys())>0):
	cursor.execute("select * from $fpkm_map")
	elements=cursor.fetchall()
	for el_ in elements:
		if(ALLOWED_GENES.get(el_[0])!=None and (len(FILTERED_GENES.keys())==0 or FILTERED_GENES.get(el_[0])!=None)):
			unique_k[el_[0]]=1
			cmd="data.addRow(["
                        cmd=add_header(cmd,el_)+"\\""+el_[1]+"\\""+","
			for x in range(2,len(el_),3):
				cmd=cmd+str(el_[x])
				if(x!=(len(el_)-3)):
					cmd=cmd+","
			print cmd+"]);"
			found_match=True
elif(len(FILTERED_GENES.keys())>0):
        cursor.execute("select * from $fpkm_map")
        elements=cursor.fetchall()
        for el_ in elements:
                if(x1=="---" and x2=="---" and x3=="---" and x4=="---" and FILTERED_GENES.get(el_[0])!=None):
                        unique_k[el_[0]]=1
                        cmd="data.addRow(["
                        cmd=add_header(cmd,el_)+"\\""+el_[1]+"\\""+","
                        for x in range(2,len(el_),3):
                                cmd=cmd+str(el_[x])
                                if(x!=(len(el_)-3)):
                                        cmd=cmd+","
                        print cmd+"]);"
                        found_match=True
 			

uk=unique_k.keys()
cursor.execute("delete from $download_map")
for unique_k_ in uk:
	cursor.execute("insert into $download_map VALUES (%s)",[unique_k_])

if(found_match==False):
	print "<h1>Unfortunately we could not find any match to the project related sequences</h1>"
a=\"\"\"
  options['page'] = 'enable';
  options['pageSize'] = 50;
  options['pagingSymbols'] = {prev: 'prev', next: 'next'};
  options['pagingButtonsConfiguration'] = 'auto';
  options['allowHtml'] = true;

  var stringFilter = new google.visualization.ControlWrapper({
    'controlType': 'StringFilter',
    'containerId': 'control1',
    'options': {
      'filterColumnLabel': 'Gene ontology terms'
    }
  });

  var table = new google.visualization.Table(document.getElementById('table_div'));
  var formatter = new google.visualization.TableColorFormat();
  formatter.addRange(0,0.001,'black','#D0D0D0');
  formatter.addRange(0.001,$filter1, 'black', '#ADD8E6');
  formatter.addRange($filter1,$filter2, 'black',  '#13DBED');
  formatter.addRange($filter2,$filter3, 'black',  '#13ED92');
  formatter.addRange($filter3,$filter4, 'black',  '#13ED3F');
  formatter.addRange($filter4,$filter5, 'black',  '#67ED13');
  formatter.addRange($filter5,$filter6, 'black',  '#BEED13');
  formatter.addRange($filter6,$filter7, 'black',  '#EDDB13');
  formatter.addRange($filter7,$filter8, 'black',  '#ED9913');
  formatter.addRange($filter8,$filter9, 'black',  '#ED6A13');
  formatter.addRange($filter9,$filter10, 'black', '#ED2C13');


 for (var j=0;j<=nmb_L;j++){
       formatter.format(data, j);
 }

table.draw(data,options);
google.visualization.events.addListener(table, 'select', selectHandler);

function selectHandler() {
    var selection = table.getSelection();
    var message = '';
    for (var i = 0; i < selection.length; i++) {
	var item = selection[i];
      if(item.row != null){
        var cur_f=data.getValue(item.row,0);
        var str = data.getFormattedValue(item.row, 0);
        message = str;
      }
    }
    if (message == '') {
      message = 'nothing';
    }else{
	    window.open("gene_report.cgi?gene="+message);
    }
  }
  visualization = new google.visualization.Table(document.getElementById('table'));
  draw();
}

function draw() {
  visualization.draw(table, options);
}

</script>
<link rel="stylesheet" type="text/css" href="$css_path">
<div id="table_div"></div>
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
t=string.Template(a)
s=t.substitute(vars())
print s




