# RNASeqExpressionBrowser

We prepared a script "installation_demo.sh" in order to generate a demo example of installation of RNASeqExpressionBrowser.
Otherwise, if actual project data should be used, this can be done by following the command
"python installation.py installation_example.conf" and modifying the textfile "installation_example.conf"


# Installation process

In order to run the tool, it needs to install goatools and needs to normally to have root permission (can also
work if the root would permit writing permission to the /var/www/cgi-bin folder and /var/www/html).

0) installation of mysql, good tutorial over here:
https://www.wikihow.com/Install-MySQL-on-Fedora

A) Goatools installation
should work with
'pip install goatools'

B) GO tools obo file
Can be obtained over here:
http://www.geneontology.org/page/download-ontology
or using the the default version under go
cd go
unzip gene_ontology.1_2.zip

B) Installation of the tool
python installation.py installation_example.conf








# Citation

RNASeqExpressionBrowser--a web interface to browse and visualize high-throughput expression data.
Nussbaumer T1, Kugler KG1, Bader KC1, Sharma S1, Seidel M1, Mayer KF1.
<a href='https://www.ncbi.nlm.nih.gov/pubmed/24833805'>RNASeqExpressionBrowser</a>
