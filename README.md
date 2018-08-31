# RNASeqExpressionBrowser

We prepared a script "installation_demo.sh" in order to generate a demo example of installation of RNASeqExpressionBrowser.
Otherwise, if actual project data should be used, this can be done by following the command
"python installation.py installation_example.conf" and modifying the textfile "installation_example.conf"

# Docker configuration (ongoing, not finished yet)

It is necessary to install docker using e.g. yum in fedora.

the script creates then a directory during the installation process, where the docker
can be started then with 

docker run -d -p 8082:80 rnaseqexpressionbrowser

where the website can be then displayed using 

http://localhost:8082/test.html


# Installation process

In order to run the tool, it needs to install goatools and needs to normally to have root permission (can also
work if the root would permit writing permission to the /var/www/cgi-bin folder and /var/www/html).

0) installation of mysql, good tutorial over here:
https://www.wikihow.com/Install-MySQL-on-Fedora

When MySQL is installed, you need to give a user and password, so that
someone can access the database where the data is stored:

e.g. CREATE USER 'newuser'@'localhost' IDENTIFIED BY 'password';
You can find a good tutorial over here: 
https://www.digitalocean.com/community/tutorials/how-to-create-a-new-user-and-grant-permissions-in-mysql
also don't forget to grant permissions:
GRANT ALL PRIVILEGES ON * . * TO 'newuser'@'localhost';

python2-mysql might be needed eventually:
yum install python2-mysql


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
