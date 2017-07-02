import string
import os
import sys
sys.path.append("tools")
from os.path import basename
import commands
import check_configuration
import subprocess
import readline, glob

def complete(text, state):
    return (glob.glob(text+'*')+[None])[state]

readline.set_completer_delims(' \t\n;')
readline.parse_and_bind("tab: complete")
readline.set_completer(complete)


#
# Check whether BLAST executables exist (blastn, makeblastdb)
#
def blast_config():
	print "--------------------------------------------"
	print "running BLAST configuration"
	print "--------------------------------------------"

	missing=False

	blast_path=""

	try:
		stdout_string = subprocess.check_output(["makeblastdb", "-h"], stderr=subprocess.STDOUT)
#		print(stdout_string)
	except subprocess.CalledProcessError as cpe:
		print(cpe.returncode)
		print(cpe.output)
		missing=True
	except OSError as e:
		if e.errno == os.errno.ENOENT:
			missing=True
		else:
			missing=True

        try:    
                stdout_string = subprocess.check_output(["blastn", "-h"], stderr=subprocess.STDOUT)
#                print(stdout_string)
        except subprocess.CalledProcessError as cpe:
                print(cpe.returncode)
                print(cpe.output)
                missing=True 
        except OSError as e:
                if e.errno == os.errno.ENOENT:
                        missing=True
                else:
                        missing=True

	if(missing==True):
	       	abort=False
	        while(abort==False):

	                user_input = raw_input(">Please specify the absolute path to ncbi-blast-Xx+/bin e.g. [/nfs/plantsp/webblast/data/ncbi-blast-2.2.27+/bin]\n") or my_input;
	                p1=user_input+"/makeblastdb"
	                p2=user_input+"/blastn"
	                o1=commands.getstatusoutput(p1)
	                o2=commands.getstatusoutput(p2)
	                if(o1[0]==256 and o2[0]==256):
	                        print "Blast configuration done"
	                        abort=True
				blast_path=user_input
	                else:
	                        abort=False
			break
	return blast_path

#
# GO terms and GO offspring terms
#
def parse_go_map(project_name,db,go_map,user,password,host):
        fh=file(go_map)
	go_map_i={}
	for line in fh.readlines():
		line=line.strip()
		vals=line.split()
		if(len(vals)>1):
			go_map_i[vals[0]]=vals[1]

        fh=file(go_map)
        i=0
        entries=[]
        h=[]
        fw=file("sql.import","w")
	fw.write("SET autocommit=0 ;");
        for line in fh.readlines():
                line=line.strip()
                vals=line.split()
                i=i+1
                if(i==1):
                        h=vals
                else:
			if(len(line)>0):
	                        entries.append(line)

        cmd="DROP TABLE IF EXISTS "+db+"."+project_name+"GO;"+"\n"
        fw.write(cmd)
        cmd="CREATE TABLE "+db+"."+project_name+"GO (go_id VARCHAR(50),go_offspring VARCHAR(20000),PRIMARY KEY(go_id)) ENGINE=MyISAM;"
        fw.write(cmd+"\n")
        for e_ in entries:
                cmd="INSERT INTO "+db+"."+project_name+"GO VALUES ( "
                v=e_.split()
                for x in range(0,len(v)):
                        v_=v[x]
			cmd=cmd+"'"+v_+"'"
                        if(x<(len(v)-1)):
                                cmd=cmd+","
                cmd=cmd+");"
                fw.write(cmd+"\n")
        fw.write(" COMMIT;");
	fw.close()
	if(len(password)==0):
		os.system("mysql --quick --host "+host+" --user "+user+" < sql.import")
	else:
                os.system("mysql --quick --host "+host+" --user "+user+" -p"+str(password)+" < sql.import")
        return go_map_i

#
# Integration of FPKM/expression values into the database
#
def parse_fpkm_map(project_name,db,fpkm_map,user,password,host):
	fh=file(fpkm_map)
	i=0
	entries=[]
	h=[]
	fw=file("sql.import","w")
        fw.write("SET autocommit=0 ;");
	for line in fh.readlines():
		line=line.strip()
		vals=line.split()
		i=i+1
		if(i==1):
			h=vals
		else:
			entries.append(line)

	cmd="DROP TABLE IF EXISTS "+db+"."+project_name+";"+"\n"
	fw.write(cmd)
	cmd="CREATE TABLE "+db+"."+project_name+" (transcript VARCHAR(50),gene VARCHAR(50),"

	conf_exist=False
	for x in range(2,len(h)):
		h_=h[x]
                if(h_.find("_conf_lo")!=-1 or h_.find("_conf_hi")!=-1 or h_.find("_LOW")!=-1 or h_.find("_HIGH")!=-1):
			conf_exist=True
	for x in range(2,len(h)):
		cmd=cmd+h[x]+" DOUBLE"
		if(conf_exist==False):
			cmd=cmd+","+h[x]+"_conf_lo DOUBLE"	
			cmd=cmd+","+h[x]+"_conf_hi DOUBLE"
		if(x<(len(h)-1)):
			cmd=cmd+","
	cmd=cmd+",PRIMARY KEY(transcript)) ENGINE=MyISAM;"
	fw.write(cmd+"\n")
	all_v=[]
	for e_ in entries:
		cmd="INSERT INTO "+db+"."+project_name+" VALUES ( "
		v=e_.split()
		for x in range(0,len(v)):
			v_=v[x]
			if(x<2):
				cmd=cmd+"'"+v_+"'"
			else:
				cmd=cmd+str(round(float(v_),1))
				if(float(v_)>0):
					all_v.append(float(float(v_)))
				if(conf_exist==False):
                                        all_v.append(float(float(v_)))
                                       	all_v.append(float(float(v_)))
	                                cmd=cmd+","+str(round(float(v_),1))
	                                cmd=cmd+","+str(round(float(v_),1))
			if(x<(len(v)-1)):
				cmd=cmd+","
		cmd=cmd+");"
		fw.write(cmd+"\n")
        fw.write(" COMMIT;");
	fw.close()

        if(len(password)==0):
                os.system("mysql --quick --host "+host+" --user "+user+" < sql.import")
        else:
                os.system("mysql --quick --host "+host+" --user "+user+" -p"+str(password)+" < sql.import")

	ak=all_v
	ak.sort()

	hF=[]

	for h_ in h:
		if(h_.find("_conf_lo")==-1 and h_.find("_conf_hi")==-1 and h_.find("_LOW")==-1 and h_.find("_HIGH")==-1):
			hF.append(h_)
	return (string.join(hF,","),ak)

#
# Integration of the domain information into the database
#
def parse_DOM(project_name,db,domain_map,go_map,user,password,host):
        fh=file(domain_map)
        i=0
        entries=[]
        cmd="DROP TABLE IF EXISTS "+db+"."+project_name+"DOM;"
        fw=file("sql.import","w")
        fw.write("SET autocommit=0 ;");
        fw.write(cmd+"\n")
        cmd="CREATE TABLE "+db+"."+project_name+"DOM (transcript VARCHAR(50), domain VARCHAR(50), PRIMARY KEY(transcript,domain), FOREIGN KEY(transcript) REFERENCES "+db+"."+project_name+") ENGINE=MyISAM;";
        for line in fh.readlines():
                line=line.strip()
                vals=line.split("\t")
                i=i+1
                if(i==1):
                        h=vals
                else:
			if(len(line)>0):
	                        entries.append(line)
        fw.write(cmd+"\n")
        for e_ in entries:
                cmd="INSERT INTO "+db+"."+project_name+"DOM VALUES ( "
		e_=e_.replace("'","\\'")
                v=e_.split("\t")
                for x in range(0,len(v)):
                        v_=v[x]
			cmd=cmd+"'"+v_+"'"
                        if(x<1):
                                cmd=cmd+","
                cmd=cmd+");"
                fw.write(cmd+"\n")
        fw.write(" COMMIT;");
        fw.close()

        if(len(password)==0):
                os.system("mysql --quick --host "+host+" --user "+user+" < sql.import")
        else:
                os.system("mysql --quick --host "+host+" --user "+user+" -p"+str(password)+" < sql.import")

        return string.join(h,",")

#
# Integration of the module information into the database
#
def parse_module(project_name,db,module_map,user,password,host):
        fh=file(module_map)
        i=0
        entries=[]
        cmd="DROP TABLE IF EXISTS "+db+"."+project_name+"MODULE;"
        fw=file("sql.import","w")
        fw.write("SET autocommit=0 ;");
        fw.write(cmd+"\n")
        cmd="CREATE TABLE "+db+"."+project_name+"MODULE (transcript VARCHAR(50), module VARCHAR(50), isHub VARCHAR(50), PRIMARY KEY(transcript,module), FOREIGN KEY(transcript) REFERENCES "+db+"."+project_name+") ENGINE=MyISAM;";
        for line in fh.readlines():
                line=line.strip()
                vals=line.split()
                i=i+1
                if(i==1):
                        h=vals
                else:
                        entries.append(line)
        fw.write(cmd+"\n")
        for e_ in entries:
                cmd="INSERT INTO "+db+"."+project_name+"MODULE VALUES ( "
                v=e_.split()
                for x in range(0,len(v)):
                        v_=v[x]
                        cmd=cmd+"'"+v_+"'"
                        if(x<=1):
                                cmd=cmd+","
                cmd=cmd+");"
                fw.write(cmd+"\n")
        fw.write(" COMMIT;");
        fw.close()

        if(len(password)==0):
                os.system("mysql --quick --host "+host+" --user "+user+" < sql.import")
        else:
                os.system("mysql --quick --host "+host+" --user "+user+" -p"+str(password)+" < sql.import")

        return string.join(h,",")

#
# Integration of the deg information into the database
#
def parse_deg(project_name,db,deg_map,user,password,host):
        fh=file(deg_map)
        i=0
        entries=[]
        cmd="DROP TABLE IF EXISTS "+db+"."+project_name+"DEG;"
        fw=file("sql.import","w")
        fw.write("SET autocommit=0 ;");
        fw.write(cmd+"\n")
        cmd="CREATE TABLE "+db+"."+project_name+"DEG (transcript VARCHAR(50), comparison VARCHAR(50), PRIMARY KEY(transcript,comparison), FOREIGN KEY(transcript) REFERENCES "+db+"."+project_name+") ENGINE=MyISAM;";
        for line in fh.readlines():
                line=line.strip()
                vals=line.split()
                i=i+1
                if(i==1):
                        h=vals
                else:
                        entries.append(line)
        fw.write(cmd+"\n")
        for e_ in entries:
                cmd="INSERT INTO "+db+"."+project_name+"DEG VALUES ( "
                v=e_.split()
                for x in range(0,len(v)):
                        v_=v[x]
                        cmd=cmd+"'"+v_+"'"
                        if(x<=0):
                                cmd=cmd+","
                cmd=cmd+");"
                fw.write(cmd+"\n")
        fw.write(" COMMIT;");
        fw.close()

        if(len(password)==0):
                os.system("mysql --quick --host "+host+" --user "+user+" < sql.import")
        else:
                os.system("mysql --quick --host "+host+" --user "+user+" -p"+str(password)+" < sql.import")

        return string.join(h,",")

#
# Integration of the deg information into the database
#
def parse_promoter(project_name,db,promoter_map,user,password,host):
        fh=file(promoter_map)
        i=0
        entries=[]
        cmd="DROP TABLE IF EXISTS "+db+"."+project_name+"PROMOTER;"
        fw=file("sql.import","w")
        fw.write("SET autocommit=0 ;");
        fw.write(cmd+"\n")
        cmd="CREATE TABLE "+db+"."+project_name+"PROMOTER (transcript VARCHAR(50), promoter VARCHAR(50), PRIMARY KEY(transcript,promoter), FOREIGN KEY(transcript) REFERENCES "+db+"."+project_name+") ENGINE=MyISAM;";
        for line in fh.readlines():
                line=line.strip()
                vals=line.split()
                i=i+1
                if(i==1):
                        h=vals
                else:
                        entries.append(line)
        fw.write(cmd+"\n")
        for e_ in entries:
                cmd="INSERT INTO "+db+"."+project_name+"PROMOTER VALUES ( "
                v=e_.split()
                for x in range(0,len(v)):
                        v_=v[x]
                        cmd=cmd+"'"+v_+"'"
                        if(x<=0):
                                cmd=cmd+","
                cmd=cmd+");"
                fw.write(cmd+"\n")
        fw.write(" COMMIT;");
        fw.close()

        if(len(password)==0):
                os.system("mysql --quick --host "+host+" --user "+user+" < sql.import")
        else:
                os.system("mysql --quick --host "+host+" --user "+user+" -p"+str(password)+" < sql.import")

        return string.join(h,",")

#
# Comment-box functionality
#
def parse_COMMENTS(project_name,db,user,password,host):
        i=0
        entries=[]
        h=[]
        cmd="DROP TABLE IF EXISTS "+db+"."+project_name+"COMMENTS;"
        fw=file("sql.import","w")
        fw.write("SET autocommit=0 ;");
        fw.write(cmd+"\n")
        cmd="CREATE TABLE "+db+"."+project_name+"COMMENTS (transcript VARCHAR(50),comments VARCHAR(1000000),PRIMARY KEY(transcript),FOREIGN KEY(transcript) REFERENCES "+db+"."+project_name+") ENGINE=MyISAM;";
	fw.write(cmd+"\n")
        fw.write(" COMMIT;");
        fw.close()

        if(len(password)==0):
                os.system("mysql --quick --host "+host+" --user "+user+" < sql.import")
        else:
                os.system("mysql --quick --host "+host+" --user "+user+" -p"+str(password)+" < sql.import")
        return string.join(h,",")

#
# Comment-box functionality
#
def parse_SEQ_NT(project_name,db,user,password,transcripts,host):
        i=0
        entries=[]
        h=[]
        cmd="DROP TABLE IF EXISTS "+db+"."+project_name+"SEQ_NT;"
        fw=file("sql.import","w")
        fw.write("SET autocommit=0 ;");
        fw.write(cmd+"\n")
        cmd="CREATE TABLE "+db+"."+project_name+"SEQ_NT (transcript VARCHAR(50),sequence VARCHAR(1000000000),PRIMARY KEY(transcript),FOREIGN KEY(transcript) REFERENCES "+db+"."+project_name+") ENGINE=MyISAM;";

        fw.write(cmd+"\n")

	fh=file(transcripts)
	sq={}
	for line in fh.readlines():
		line=line.strip()
		if(line.find(">")!=-1):
			cid=line[1:].split()[0]
			assert(sq.get(cid)==None)
			sq[cid]=""
		else:
			sq[cid]=sq[cid]+line

	for sq_ in sq:
		cmd="INSERT INTO "+db+"."+project_name+"SEQ_NT VALUES ('"+sq_+"','"+sq[sq_]+"');"
		fw.write(cmd+"\n")

	fw.write(" COMMIT;");
	fw.close()

        if(len(password)==0):
                os.system("mysql --quick --host "+host+" --user "+user+" < sql.import")
        else:
                os.system("mysql --quick --host "+host+" --user "+user+" -p"+str(password)+" < sql.import")
        return string.join(h,",")


#
# Comment-box functionality
#
def parse_SEQ_AA(project_name,db,user,password,transcripts,host):
        i=0
        entries=[]
        h=[]
        cmd="DROP TABLE IF EXISTS "+db+"."+project_name+"SEQ_AA;"
        fw=file("sql.import","w")
        fw.write("SET autocommit=0 ;");
        fw.write(cmd+"\n")
        cmd="CREATE TABLE "+db+"."+project_name+"SEQ_AA (transcript VARCHAR(50),sequence VARCHAR(1000000000),PRIMARY KEY(transcript),FOREIGN KEY(transcript) REFERENCES "+db+"."+project_name+") ENGINE=MyISAM;";

        fw.write(cmd+"\n")

        fh=file(transcripts)
        sq={}
        for line in fh.readlines():
                line=line.strip()
                if(line.find(">")!=-1):
                        cid=line[1:].split()[0]
                        assert(sq.get(cid)==None)
                        sq[cid]=""
                else:
                        sq[cid]=sq[cid]+line

        for sq_ in sq:
                cmd="INSERT INTO "+db+"."+project_name+"SEQ_AA VALUES ('"+sq_+"','"+sq[sq_]+"');"
                fw.write(cmd+"\n")

        fw.write(" COMMIT;");
        fw.close()

        if(len(password)==0):
                os.system("mysql --quick --host "+host+" --user "+user+" < sql.import")
        else:
                os.system("mysql --quick --host "+host+" --user "+user+" -p"+str(password)+" < sql.import")
        return string.join(h,",")


#
# DOWNLOAD functionality
#
def parse_DOWNLOAD(project_name,db,user,password,host):
        i=0
        entries=[]
        h=[]
        cmd="DROP TABLE IF EXISTS "+db+"."+project_name+"DOWNLOAD;"
        fw=file("sql.import","w")
        fw.write("SET autocommit=0 ;");
        fw.write(cmd+"\n")
        cmd="CREATE TABLE "+db+"."+project_name+"DOWNLOAD (transcript VARCHAR(50),PRIMARY KEY(transcript),FOREIGN KEY(transcript) REFERENCES "+db+"."+project_name+") ENGINE=MyISAM;";
        fw.write(cmd+"\n")
        fw.write(" COMMIT;");
        fw.close()

        if(len(password)==0):
                os.system("mysql --quick --host "+host+" --user "+user+" < sql.import")
        else:
                os.system("mysql --quick --host "+host+" --user "+user+" -p"+str(password)+" < sql.import")
        return string.join(h,",")

#
# Integration of the Human Readable Description into the database
#
def parse_HRD(project_name,db,hrd_map,user,password,host):
        fh=file(hrd_map)
        i=0
        entries=[]
        h=[]
        cmd="DROP TABLE IF EXISTS "+db+"."+project_name+"HRD;"
	fw=file("sql.import","w")
        fw.write("SET autocommit=0 ;");
        fw.write(cmd+"\n")
        cmd="CREATE TABLE "+db+"."+project_name+"HRD (transcript VARCHAR(50),description VARCHAR(10000),PRIMARY KEY(transcript), FOREIGN KEY(transcript) REFERENCES "+db+"."+project_name+") ENGINE=MyISAM;";
        for line in fh.readlines():
                line=line.strip()
                vals=line.split("\t")
                i=i+1
                if(i==1):
                        h=vals
                else:
                        entries.append(line)
        fw.write(cmd+"\n")
        for e_ in entries:
		e_=e_.replace("'","\\'")
		e_=e_.replace("\"","\\\"")
                v=e_.split("\t")
		if(len(v)==2):
	                cmd="INSERT INTO "+db+"."+project_name+"HRD VALUES ( "
	                for x in range(0,len(v)):
	                        v_=v[x]
	                        if(x<2):
	                                cmd=cmd+"\""+v_+"\""
	                        else:
	                                cmd=cmd+v_
	                        if(x<(len(v)-1)):
	                                cmd=cmd+","
	                cmd=cmd+");"
	                fw.write(cmd+"\n")
        fw.write(" COMMIT;");
        fw.close()

        if(len(password)==0):
                os.system("mysql --quick --host "+host+" --user "+user+" < sql.import")
        else:
                os.system("mysql --quick --host "+host+" --user "+user+" -p"+str(password)+" < sql.import")
        return string.join(h,",")

#
# Creating database to blast sequence against database associated transcripts
#
def parse_transcripts(project_name,transcripts_NT,transcripts_AA,blast_path,web_server_location):
	os.system("cp "+str(transcripts_NT)+" "+web_server_location+"/"+str(project_name)+"/.")
	transcripts_NT=basename(transcripts_NT)

	if(len(blast_path)>0):
		os.system("cd "+web_server_location+"/"+str(project_name)+";"+blast_path+"/makeblastdb -dbtype nucl -in "+web_server_location+"/"+str(project_name)+"/"+str(transcripts_NT))
	else:
                os.system("cd "+web_server_location+"/"+str(project_name)+";makeblastdb -dbtype nucl -in "+web_server_location+"/"+str(project_name)+"/"+str(transcripts_NT))

        os.system("cp "+str(transcripts_AA)+" "+web_server_location+"/"+str(project_name)+"/.")
        transcripts_AA=basename(transcripts_AA)

        if(len(blast_path)>0):
                os.system("cd "+web_server_location+"/"+str(project_name)+";"+blast_path+"/makeblastdb -dbtype prot -in "+web_server_location+"/"+str(project_name)+"/"+str(transcripts_AA))
        else:
                os.system("cd "+web_server_location+"/"+str(project_name)+";makeblastdb -dbtype nucl -in "+web_server_location+"/"+str(project_name)+"/"+str(transcripts_AA))


#
# Parsing of the configuration file, entries separated by "::"
#
def parse_conf(f_):
	fh=file(f_)
	conf={}
	for line in fh.readlines():
		line=line.strip()
		if(line.find("::")!=-1):
			vals=line.split("::")
			conf[vals[0]]=vals[1]
			print vals[0],vals[1]
	return conf

#
# CSS copying CSS file to location under /var/www/html
#
def copy_css(webserver_name):
	pref_dir=""
	css_path=""
	found=False
	while(found==False):
		user_input = raw_input(">Please specify the absolute path to the directory where CSS file should be stored (within the /var/www/html directory, directory must exist) e.g. [/var/www/html]\n") or my_input;
		if(os.access(user_input, os.W_OK)==True):
			if(user_input.find("/var/www")!=-1):
				css_path=user_input+"/main.css"
				os.system("cp main.css "+css_path)
				css_path=webserver_name+"/"+css_path.split(user_input)[1]
				found=True
		else:
			print "You need writing permissions for this directory, run as root"
	return css_path	

#
# Web server location
#
def web_server_location():
        pref_dir=""
        web_server_path=""
        found=False
        while(found==False):
                user_input = raw_input(">Please specify the absolute path to the directory of the web server location, somewhere under e.g. [/var/www/cgi-bin OR /usr/lib/cgi-bin]\n")
                if(os.access(user_input, os.W_OK)==True):
	                if(user_input.find("/var/www/cgi-bin")!=-1 or user_input.find("/usr/lib/cgi-bin")!=-1):
	                        web_server_path=user_input
	                        found=True
		else:
			print "You need writing permissions for this directory, run as root"
        return web_server_path

#
# temporary location
#
def temp_location():
	found=False
	temp_location=""
	while(found==False):
		user_input = raw_input(">Please provide the path to the directory where R-output can be stored and accessed by apache-user e.g. [/nfs/plantsp/webblast/data/]\n")
                if(os.access(user_input, os.W_OK)==True):
			temp_location=user_input
			found=True
                else:
                        print "You need writing permissions for this directory, run as root"
 	return temp_location

#
#
#
def extract_go(map_GO,dom,obo_file):
	try:
		from goatools import obo_parser
		p = obo_parser.GODag(obo_file)
		fh=file(dom)
		gos={}
		gos2={}
		fw=file(map_GO,"w")
		for line in fh.readlines():
		        line=line.strip()
		       	vals=line.split()
			if(len(vals)>1):
			        if(vals[1].find("GO")!=-1):
	                        	gos[vals[1]]=1
		for gos_ in gos:
			gos2[gos_]=1
			CC=p[gos_].get_all_parents()
			for CC_ in CC:
				gos2[CC_]=1
		for gos_ in gos2:
		        CC=p[gos_].get_all_children()
			if(len(CC)>0):
			        fw.write(gos_+"\t"+string.join(CC,";")+"\n")
		fw.close()
	except Exception:
		print "ERROR","Python module goatools is missing"
		print sys.exc_info()
		sys.exit()

print "-------------------------------------------------------------------------"

try:
	f_=sys.argv[1]
except Exception:
	print "configuration file missing, use 'python installation.py installation.conf'"
	sys.exit()

obo_file="go/gene_ontology.1_2.obo"

check_configuration.validate(f_)

web_server_location=web_server_location()

temp_dir=temp_location()

conf=parse_conf(f_)

css_path=copy_css(conf["webserver"])
	
blast_path=blast_config()

project_name=conf["project_name"]
print "Project Name", project_name

db_name=conf["mysql_db"]
print "Mysql Database Name", db_name

hrd=conf["hrd"]
print "Mapping Gene Human Readable Description", db_name

dom=conf["dom"]
print "Gene Domain Mapping", dom

fpkm_value_matrix=conf["fpkm_value_matrix"]
print "FPKM Value Matrix", fpkm_value_matrix

if(conf.get("module")!=None):
	module_map=conf["module"]
	print "MODULE",module_map
else:
	module_map=None
	print "No MODULE were included"

if(conf.get("deg")!=None):
	deg_map=conf["deg"]
	print "DEG",deg_map
else:
	deg_map=None
	print "No DEG were included"

if(conf.get("promoter")!=None):
	promoter_map=conf["promoter"]
	print "PROMOTER",promoter_map
else:
	promoter_map=None
	print "No PROMOTER were included"

transcripts_NT=conf["transcripts_NT"]
print "transcripts_NT", transcripts_NT

transcripts_AA=conf["transcripts_AA"]
print "transcripts_AA", transcripts_AA

html_description=conf["html_description"]
print "html_decription", html_description

db_link_path=conf["db_link_path"]
print "db_link_path",db_link_path

web_server=conf["webserver"]
print "webserver",web_server

mysql_host=conf["mysql_host"]
print "mysql_host",mysql_host

mysql_user=conf["mysql_user"]
print "mysql_user",mysql_user

mysql_password=conf["mysql_password"]
print "mysql_password",mysql_password

example_gene_identifier=conf["example_gene_identifier"]
example_keyword=conf["example_keyword"]
example_go_id=conf["example_GO_ID"]
example_interpro_id=conf["example_Interpro_ID"]
example_FASTA=conf["example_FASTA"]

print "-------------------------------------------------------------------------"


print "GO mapping - extracting offspring of GO ids" 
go_map="map_GO.TXT"
extract_go(go_map,dom,obo_file) 
print "GO mapping finished"

print "parsing GO..." 
go_map=parse_go_map(project_name,db_name,go_map,mysql_user,mysql_password,mysql_host); 
print "parsing GO finished"

print "parsing FPKM..."
(header,all_v)=parse_fpkm_map(project_name,db_name,fpkm_value_matrix,mysql_user,mysql_password,mysql_host)
print "parsing FPKM finished..."

if(module_map!=None):
	print "parsing MODULE..."
	parse_module(project_name,db_name,module_map,mysql_user,mysql_password,mysql_host)

if(promoter_map!=None):
	print "parsing PROMOTER..."
	parse_promoter(project_name,db_name,promoter_map,mysql_user,mysql_password,mysql_host)

if(deg_map!=None):
	print "parsing DEG..."
	parse_deg(project_name,db_name,deg_map,mysql_user,mysql_password,mysql_host)

print "parsing COMMENTS..."
parse_COMMENTS(project_name,db_name,mysql_user,mysql_password,mysql_host)

print "parsing SEQ nucleotide sequences"
parse_SEQ_NT(project_name,db_name,mysql_user,mysql_password,transcripts_NT,mysql_host)

print "parsing SEQ amino acids"
parse_SEQ_AA(project_name,db_name,mysql_user,mysql_password,transcripts_AA,mysql_host)

print "parsing DOWNLOAD..."
parse_DOWNLOAD(project_name,db_name,mysql_user,mysql_password,mysql_host)

filter1=all_v[int(len(all_v)*0.1)]
filter2=all_v[int(len(all_v)*0.2)]
filter3=all_v[int(len(all_v)*0.3)]
filter4=all_v[int(len(all_v)*0.4)]
filter5=all_v[int(len(all_v)*0.5)]
filter6=all_v[int(len(all_v)*0.6)]
filter7=all_v[int(len(all_v)*0.7)]
filter8=all_v[int(len(all_v)*0.8)]
filter9=all_v[int(len(all_v)*0.9)]
filter10=max(all_v)

print "parsing HRD..."
parse_HRD(project_name,db_name,hrd,mysql_user,mysql_password,mysql_host);
print "parsing HRD finished..."

print "parsing DOM..."
parse_DOM(project_name,db_name,dom,go_map,mysql_user,mysql_password,mysql_host);
print "parsing DOM finished..."

print "delete temporary files"
os.system("rm map_GO.TXT")
os.system("rm sql.import")
print "-------------------------------------------------------------------------"

os.system("mkdir "+web_server_location+"/"+str(project_name))
print "parsing transcripts..."
parse_transcripts(project_name,transcripts_NT,transcripts_AA,blast_path,web_server_location);
print "Parsing transcripts finished"

print "-------------------------------------------------------------------------"

assert(len(project_name)>0)

print "-------------------------------------------------------------------------"

fpkm=db_name+"."+project_name
hrd=db_name+"."+project_name+"HRD"
dom=db_name+"."+project_name+"DOM"
go=db_name+"."+project_name+"GO"
cmt_map=db_name+"."+project_name+"COMMENTS"
seq_nt_map=db_name+"."+project_name+"SEQ_NT"
seq_aa_map=db_name+"."+project_name+"SEQ_AA"
download_map=db_name+"."+project_name+"DOWNLOAD"

print "-------------------------------------------------------------------------"

cmd="python index.cgi "+str(html_description)+" "+str(css_path)+" "+str(example_gene_identifier)+" "+str(example_keyword)+" "+str(example_go_id)+" "+str(example_interpro_id)+" "+str(example_FASTA)+" "+str(project_name)+" "+conf["hrd"]+" "+conf["dom"]+" "+obo_file+ " "+str(module_map)+" "+str(deg_map)+" "+str(promoter_map)+" > "+web_server_location+"/"+str(project_name)+"/index.cgi"
print cmd
os.system(cmd)

cmd="python search.cgi "+str(header)+" "+str(fpkm)+" "+str(hrd)+" "+str(dom)+" "+str(go)+" "+str(module_map)+" "+str(css_path)+" "+str(filter1)+" "+str(filter2)+" "+str(filter3)+" "+str(filter4)+" "+str(filter5)+" "+str(filter6)+" "+str(filter7)+" "+str(filter8)+" "+str(filter9)+" "+str(filter10)+" "+str(mysql_host)+" "+str(mysql_user)+" "+str(project_name)+" "+str(db_name)+" "+str(mysql_password)+ " > "+web_server_location+"/"+str(project_name)+"/search.cgi"
print cmd
os.system(cmd)

cmd="python gene_report.cgi "+" "+str(header)+" "+str(fpkm)+" "+str(dom)+" "+str(hrd)+" "+str(cmt_map)+" "+str(seq_nt_map)+" "+str(seq_aa_map)+" "+str(db_link_path)+" "+str(css_path)+" "+str(mysql_host)+" "+str(mysql_user)+" "+str(project_name)+" "+str(db_name)+" "+str(mysql_password)+" > "+web_server_location+"/"+str(project_name)+"/gene_report.cgi"
print cmd
os.system(cmd)

cmd="python blast.cgi"+" "+str(css_path)+" "+str(db_link_path)+" "+str(project_name)+" "+str(blast_path)+" > "+web_server_location+"/"+str(project_name)+"/blast.cgi"
print cmd
os.system(cmd)
cmd="chmod +x "+web_server_location+"/"+str(project_name)+"/blast.cgi"
print cmd
os.system(cmd)

cmd="python export.cgi "+" "+str(dom)+" "+str(fpkm)+" "+str(hrd)+" "+str(go)+" "+str(download_map)+" "+str(mysql_host)+" "+str(mysql_user)+" "+str(db_name)+" "+str(mysql_password)+" > "+web_server_location+"/"+str(project_name)+"/export.cgi"
print cmd
os.system(cmd)
cmd="chmod +x "+web_server_location+"/"+str(project_name)+"/export.cgi"
print cmd
os.system(cmd)

cmd="python action.cgi  > "+web_server_location+"/"+str(project_name)+"/action.cgi"
print cmd
os.system(cmd)
cmd="chmod +x "+web_server_location+"/"+str(project_name)+"/action.cgi"
print cmd
os.system(cmd)

content=file("comment_BOX.cgi").readlines()
content=string.join(content,"\n")
content=content.replace("__PROJECT__",project_name)
content=content.replace("__HOST__",str(mysql_host))
content=content.replace("__PASSWORD__",str(mysql_password))
content=content.replace("__USER__",str(mysql_user))
content=content.replace("__TEMP__",str(temp_dir))
content=content.replace("__DB__",str(db_name))

fw=file(web_server_location+"/"+str(project_name)+"/comment_BOX.cgi","w")
fw.write(content)
fw.close()


cmd="python help.cgi "+str(css_path)+" "+str(project_name)+ " > "+web_server_location+"/"+str(project_name)+"/help.cgi"
print cmd
os.system(cmd)
cmd="chmod 755 "+web_server_location+"/"+str(project_name)+"/help.cgi"

cmd="touch "+web_server_location+"/"+str(project_name)+"/XXX";
print cmd
os.system(cmd)
cmd="chmod 777 "+web_server_location+"/"+str(project_name)+"/XXX";
print cmd
os.system(cmd)

cmd="touch "+web_server_location+"/"+str(project_name)+"/YYY";
print cmd
os.system(cmd)
cmd="chmod 777 "+web_server_location+"/"+str(project_name)+"/YYY";
print cmd
os.system(cmd)

cmd="chmod 755 "+web_server_location+"/"+str(project_name)+"/*cgi";
print cmd
os.system(cmd)

cmd="python make_eigengenes.py "+str(mysql_host)+" "+str(mysql_user)+" "+str(mysql_password)+" "+str(project_name)+" "+str(db_name)+" "+str(css_path)+" "+str(temp_dir)+" > "+web_server_location+"/"+str(project_name)+"/eigengenes.cgi"
print cmd
os.system(cmd)

cmd="chmod 755 "+web_server_location+"/"+str(project_name)+"/"+"eigengenes.cgi"
print cmd
os.system(cmd)

cmd="python make_gene_net_R.py "+str(temp_dir)+" > "+web_server_location+"/"+str(project_name)+"/gene_net.R"
print cmd
os.system(cmd)
cmd="chmod 755 "+web_server_location+"/"+str(project_name)+"/gene_net.R"
print cmd
os.system(cmd)

cmd="python make_eigengenes_R.py "+str(temp_dir)+" > "+web_server_location+"/"+str(project_name)+"/eigengenes.R"
print cmd
os.system(cmd)
cmd="chmod 755 "+web_server_location+"/"+str(project_name)+"/eigengenes.R"
print cmd
os.system(cmd)

cmd="python export_file.py "+str(temp_dir)+" > "+web_server_location+"/"+str(project_name)+"/export_file.cgi"
print cmd
os.system(cmd)
cmd="chmod 755 "+web_server_location+"/"+str(project_name)+"/export_file.cgi"
print cmd
os.system(cmd)

print "-------------------------------------------------------------------------"


