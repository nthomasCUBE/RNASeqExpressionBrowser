import sys
css_path=sys.argv[1]
project=sys.argv[2]

a="""#!/usr/bin/env python
import cgi
import cgitb
import sys
import MySQLdb
import string

cgitb.enable()

print 'Content-type: text/html\\r\\n\\r'
"""
print a
print "print \"<html>\""
print "print \"<div class='header'>\""
print "print \"<h1><a href='index.cgi'>"+project+"</a></h1>\""
print "print \"</div>\""
a="""
a=\"\"\"
<title>Help page</title>
<body>
"""
print a
print "<link rel=\"stylesheet\" type=\"text/css\" href=\""+css_path+"\">"

a="""
<div class="help-content">
<h1><a name="index">Index</a> </h1>
<ul>
<li><a href="#gene_search">Searching for genes</a> </li><li><a href="#search_results">Working with search results</a> </li><li><a href="#single_gene">Single gene report</a> </li></ul>
<br>
&nbsp;<br>



<hr>
<h1><a name="gene_search">Searching for genes</a> </h1>
You can access your genes of interest with the following methods:
<h2>Annotation</h2>
<h3>Gene identifier</h3>
For the search via 'Gene identifier' the gene name can be queried. In addition, it is possible to search for genes using a prefix search, by using '
<i>XXX%</i> ', where ' <i>XXX</i> ' is the prefix and ' <i>%</i> ' represents the wild card.
<h3>Keyword</h3>
Using this option genes are queried based on their description line. Suggestions are provided via an autocomplete function when providing at least three characters.
<h3>Gene Ontology ID</h3>
Gene Ontology (GO) aims at standardizing the representation of gene and gene product attributes across species and databases. More details can obtained from
<a href="redir.aspx?C=Eo2--7tDUkyue5TkFWj3WEwCNpMPKdFItGWdZwPt1rsUueWFKeH_bk-f2wMC8NX_WJs7ni0Fkug.&amp;URL=http%3a%2f%2fwww.geneontology.org%2f" target="_blank">
Gene Ontology</a> . The search is based on providing the ID (e.g. GO:0006556 rather then
<i>'S-adenosylmethionine biosynthetic process</i> '), but we provide an ID to term mapping when typing at least three characters in the search field. The search considers the GO hierarchy, therefore when searching a very general term, this can lead to increased
 time for the search.
<h3>Interpro ID</h3>
Additionally, other domain information can be integrated and searched. For the search the domain id has to fully match to the provided domain terms (e.g. '
<i>IPR008147</i> ')
<h3>Network (gene-to-group information) and Differentially expressed genes plugin</h3>
With the release of version 2.0, the RNASeqExpressionBrowser also allows to integrate as well as browse for network modules and differentially expressed genes.
We aimed by integrating this feature, to browse for genes that are expressed similarity as an outcome of weighted gene co-expression network as the WGCNA, but
basically also groups of genes that share common features can be integrated.
In addition, we allow to include information of differentially expressed genes those are typically defined by tools as EdgeR or Cuffdiff. We aimed
to include pair-wise contrast (e.g. water_vs_mock), so that those genes can be nicely selected.
<br>
<br>
<b>Input format for differentially expressed genes<b>
<br>
<textarea style='width:300px;background:lightblue' rows="5">
gene	comparison
MLOC_30	water_vs_mock
MLOC_50 water_vs_heat
MLOC_50 drought_vs_heat
</textarea>
<br>
<br>
<b>Input format for network modules (gene-to-group assignments)<b>
<br>
<textarea style='width:300px;background:lightblue' rows="5">
gene	module	isHub
MLOC_30	green	TRUE
MLOC_50	green	FALSE
MLOC_70	red	FALSE
</textarea>
<br>
<br>
Apart from the gene-to-group assignments, also a third column is listed. This column 'isHub' represents a flag, for genes that are representative for the whole
module. You might thinkof genes that activate other genes and might have therefore some regulation effect. In a network representation those genes
represent typically highly-connected genes, the so caled hub genes.

<h2>Sequence similarity</h2>
A Blast search against project associated sequences is provided, allowing searching multiple nucleotide sequences in a nucleotide database, which was provided during the installation. In addition to the FASTA sequences the user can select a threshold for the
 Expect(E) Value. The search result reports the sequence identity, the bp length of the match and the BLAST score. Note, that only report genes with available expression information are reported.
<br>
<h2>List of gene id</h2>
If you want to search for particular gene identifiers, you can provide multiple gene identifiers. Gene identifiers need to be separated by a new line, e.g.:
<br>
<textarea style='width:300px;background:lightblue' rows="5">
MLOC_XXX
MLOC_YYY
</textarea>
<br>
<p><a href="#index">back to index</a> </p>
<hr>
<h1><a name="search_results">Working with search results</a> </h1>
The page lists the results returned by the gene search. The strength of expression is color coded as shown in the top legend on the page. If the list of reported genes is too long it will be split into several smaller parts, which can be accessed using the
 page navigation below the table. When selecting a row, the selected gene information will be displayed on an extra page. Genes in the search results can be re-ordered by selecting the corresponding column header. Additionally, the listed information can be
 downloaded with the <i>Download</i> option on the top left.
<p><a href="#index">back to index</a> </p>


<hr>
<h1><a name="single_gene">Single gene report</a> </h1>
This page reports expression and annotation information for a single gene. The expression information is displayed both as a bar chart and and in a tabular form. Below the expression information additional annotations (domains and gene ontology terms) are displayed.
 If provided during the installation also a link to an external database will be displayed.
<p><a href="#index">back to index</a> </p>
</div>
<div class="footer">
<p>This web site was created with <a href="redir.aspx?C=Eo2--7tDUkyue5TkFWj3WEwCNpMPKdFItGWdZwPt1rsUueWFKeH_bk-f2wMC8NX_WJs7ni0Fkug.&amp;URL=http%3a%2f%2fmips.helmholtz-muenchen.de%2fplant%2fRNASeqExpressionBrowser%2findex.jsp" target="_blank">
RNAExpressionBrowser</a> </p>
</div>
</body>
</html>
\"\"\"
print a
"""
print a
