import string
import sys

# ------------------------------------------------------------------------------------------

html_description=sys.argv[1]
css_path=sys.argv[2]
example_gene_identifier=sys.argv[3]
example_keyword=sys.argv[4]
example_go_id=sys.argv[5]
example_interpro_id=sys.argv[6]
example_fasta=sys.argv[7]
project_name=sys.argv[8]
hrd_map=sys.argv[9]
go_map=sys.argv[10]
obo_file=sys.argv[11]
module_map=sys.argv[12]
deg_map=sys.argv[13]
prom_map=sys.argv[14]

# ------------------------------------------------------------------------------------------


a="""#!/usr/bin/env python
import cgi
import cgitb
import sys
cgitb.enable()

print 'Content-type: text/html\\r\\n\\r'

a=\"\"\"
<link rel="stylesheet" href="//code.jquery.com/ui/1.10.4/themes/smoothness/jquery-ui.css">
<script src="//code.jquery.com/jquery-1.9.1.js"></script>
<script src="//code.jquery.com/ui/1.10.4/jquery-ui.js"></script>
\"\"\"
print a

"""
print a

a="""
a=\"\"\"
<script>
function displayResult(id,helpid,  headerid){
        var availableTags = [
"""
print a

fh=file(hrd_map)
uu={}
for line in fh.readlines():
	line=line.strip()
	vals=line.split("\t")
	if(len(vals)==2):
		c_t=vals[1].replace("\"","'")
		if(uu.get(c_t)==None):
			print "\""+c_t+"\",",
		uu[c_t]=1
a="""
		''
        ];

	var availableTags2 = [
"""
print a

from goatools import obo_parser
p = obo_parser.GODag(obo_file)
fh=file(go_map)
gos={}
gos2={}
for line in fh.readlines():
        line=line.strip()
        vals=line.split()
	if(len(vals)>1):
		if(vals[1].find("GO:")!=-1):
			gos[vals[1]]=1
for gos_ in gos:
	gos2[gos_]=1
	CC=p[gos_].get_all_parents()
	for CC_ in CC:
		gos2[CC_]=1
for gos_ in gos2:
	c_t=gos_+" "+str(p[gos_].name)
        print "\""+c_t+"\",",
print "''"

a="""

	];

        $('#search2').autocomplete({
                source: availableTags,
		minLength:3
        });
	$('#search3').autocomplete({
		source: availableTags2,
		minLength:3
	});
	

"""
print a
print "$(\"#example\").click(function () {"
print "$(\"#fasta\").val(\""+example_fasta+"\")"
print "});"

a="""

			document.getElementById('getkey').style.display = "none";
			document.getElementById('getseq').style.display = "none";
			document.getElementById('getlist').style.display = "none";
			document.getElementById(id).style.display = "block";

			document.getElementById('helpkey').style.display = "none";
			document.getElementById('helpseq').style.display = "none";
			document.getElementById('helplist').style.display = "none";
			document.getElementById(helpid).style.display = "block";

			document.getElementById('headerkey').className = "headerinact";
			document.getElementById('headerseq').className = "headerinact";
			document.getElementById('headerlist').className = "headerinact";
			document.getElementById(headerid).className = "headeract";
}
</script>
"""
print a

a="""
<body onload="displayResult('getkey','helpkey','headerkey')">
<div class="header">
<h1><a href="index.cgi">$project_name</a></h1>
<title>$project_name</title>
<link rel="stylesheet" type="text/css" href="$css_path"/>
</div>
	<div class="content">
		<div id="content-menu">
			<table>
				<tbody>
					<tr style="text-align: center;">
						<td id="headerkey" class="headeract" style="min-width: 160px;"><a
							class="anone" href="#"
							onclick="displayResult('getkey','helpkey','headerkey')">Keywords</a></td>
						<td id="headerseq" class="headerinact" style="min-width: 160px;"><a
							class="anone" href="#"
							onclick="displayResult('getseq','helpseq','headerseq')">Blast</a></td>
						<td id="headerlist" class="headerinact" style="min-width: 160px;"><a
							class="anone" href="#"
							onclick="displayResult('getlist','helplist','headerlist')">Gene
								List Search</a></td>
						<td class="headerinact" style="width: 100%;">&nbsp;</td>
						<td id="headerseq" class="headerinact" style="min-width: 160px;"><a
							class="anone" target="_blank" href="./help.cgi">Help</a></td>
					</tr>
				</tbody>
			</table>
			<div id="helpkey" class="content-menu-help"
				style="visibility: visible;">Search for your genes of interest
				using either identifiers or annotations</div>
			<div id="helpseq" class="content-menu-help" style="display: none;">
				Search for your genes of interest using FASTA sequences
			</div>
			<div id="helplist" class="content-menu-help" style="display: none;">Enter
				a list of gene identifiers that you want to select</div>
		</div>
		<div class="container">

			<!--  SEARCH BY KEYWORDS -->

			<form id="getkey" style="display: block;"
				action="search.cgi"
				method="get">
				<table>
					<tbody>
						<tr>
							<td style="text-align: right;">Gene Identifier</td>
							<td><input type="text" name="search" size="48"></td>
							<td class="example">"$example_gene_identifier"</td>
						</tr>
						<tr>
							<td style="text-align: right;">Keyword</td>
							<td><input id="search2" type="text" name="search2" size="48"></td>
							<td class="example">"$example_keyword"</td>
						</tr>
						<tr>
							<td style="text-align: right;">GO ID</td>
							<td><input id="search3" type="text" name="search3" size="48"></td>
							<td class="example">"$example_go_id"</td>
						</tr>
						<tr>
							<td style="text-align: right;">Interpro ID</td>
							<td><input type="text" name="search4" size="48"></td>
							<td class="example">"$example_interpro_id"</td>
						</tr>
                                                <tr>
                                                        <td style='text-align:right;'>Comment search</td>
                                                        <td><input id='comment' name='comment' size="48"></td>
							<td><a href='comment_BOX.cgi'>Show comments</a></td>
                                                </tr>

"""
t=string.Template(a)
s=t.substitute(vars())
print s

if(module_map!="None"):
	fh=file(module_map)
	MODULE={}
	i=0
	for line in fh.readlines():
		line=line.strip()
		vals=line.split()
		i=i+1
		if(i>1):	
			MODULE[vals[1]]=1
	
	print "<tr>"
	print "<tr>"
	print "<td style='text-align:right'>gene-to-group mapping</td>"
	print "<td>"
	print "<select style='width:250px' name='module' id='module' >"
	print "<option>---</option>"
	MK=MODULE.keys()
	MK.sort()
	for MODULE_ in MK:
		print "<option>",MODULE_,"</option>"
	print "</select>"
	print "</td>"
	print "<td>"
	print "<input type='checkbox' name='hub' id='hub'>"
	print "<label>Hub Genes only</label>"
	print "</td>"
	print "</tr>"

if(deg_map!="None"):
	fh=file(deg_map)
	DEG={}
	i=0
	for line in fh.readlines():
        	line=line.strip()
        	vals=line.split()
        	i=i+1
	        if(i>1):
	                DEG[vals[1]]=1
	print "<tr>"
	print "<td style='text-align:right'>DEG lists</td>"
	print "<td>"
	print "<select style='width:250px' name='module2' id='module'>"
	print "<option>---</option>"
	DK=DEG.keys()
	DK.sort()
	for DK_ in DK:
		print "<option>",DK_,"</option>"
	print "</select>"
	print "</td>"
	print "</tr>"

if(prom_map!="None"):
	fh=file(prom_map)
	PROM={}
	i=0
	for line in fh.readlines():
	       	line=line.strip()
	        vals=line.split()
	        i=i+1	
	        if(i>1):
	                PROM[vals[1]]=1
	print "<tr>"
	print "<td style='text-align:right'>Promoter</td>"
	print "<td>"
	print "<select style='width:250px' name='promoter' id='promoter'>"
	print "<option>---</option>"
	PK=PROM.keys()
	PK.sort()	
	for PK_ in PK:
	        print "<option>",PK_,"</option>"
	print "</select>"
	print "</td>"
	print "</tr>"


a="""
                                                <tr>
                                                        <td>&nbsp;</td>
                                                        <td><input type="reset" value="Reset"> <input
                                                                type="submit" value="Submit"></td>
                                                        <td>&nbsp;</td>
                                                </tr>

					</tbody>
				</table>
			</form>

			<!--  SEARCH BY BLAST -->

			<form id="getseq" style="display: none;" action="blast.cgi"
				method="post" accept-charset="ISO-8859-1">
				<table>
					<tbody>
						<tr>
							<td style="text-align: right;">FASTA Sequence</td>
							<td><textarea rows="6" cols="80" name="fasta" id="fasta"></textarea></td>
						</tr>
						<tr>
							<td style="text-align: right;">Expect (E) Value</td>
							<td><select name="eval">
                                                                        <option value="10e-0">10e-0</option>
									<option value="10e-5">10e-5</option>
									<option value="10e-10">10e-10</option>
									<option value="10e-15">10e-15</option>
									<option value="10e-20">10e-20</option>
									<option value="10e-25">10e-25</option>
                                                                        <option value="10e-30">10e-30</option>
                                                                        <option value="10e-35">10e-35</option>
                                                                        <option value="10e-40">10e-40</option>
                                                                        <option value="10e-45">10e-45</option>
							</select></td>
						</tr>
						<tr>
							<td style="text-align: right;">Program</td>
							<td><select name="program">
									<option>BLASTN</option>
									<option>BLASTP</option>
							</select></td>	
						</tr>
						<tr>
							<td>&nbsp;</td>
							<td>                                
								<input type="button" value="example" id="example" />
								<input type="reset" value="Reset"> 
								<input type="submit" value="Submit"></td>
						</tr>
					</tbody>
				</table>
			</form>

			<!--  SEARCH BY GENE LIST -->

			<form id="getlist" style="display: none;" action="action.cgi"
				method="post">
				<table>
					<tbody>
						<tr>
							<td style="text-align: right;">Gene Identifier</td>
							<td><textarea rows="6" cols="80" name="goids"></textarea></td>
						</tr>
						<tr>
							<td>&nbsp;</td>
							<td><input type="reset" value="Reset"> <input
								type="submit" value="Submit"></td>
						</tr>
					</tbody>
				</table>
			</form>
		</div>
	</div>
<br/>
<br/>
\"\"\"
print a
"""
t=string.Template(a)
s=t.substitute(vars())
print s

fh=file(html_description)
for line in fh.readlines():
	line=line.strip()
	print "print '"+line+"'"
a="""
a=\"\"\"
	<br/>
        <div class="footer">
                <p>
                        This web site was created with <a
                                href="http://mips.helmholtz-muenchen.de/plant/RNASeqExpressionBrowser/index.jsp"
                                target="_blank">RNAExpressionBrowser</a>
                </p>
        </div>
\"\"\"
print a
"""
print a

