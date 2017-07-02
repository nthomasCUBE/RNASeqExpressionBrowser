import os
import sys


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
        return conf


def validate(c_f):

	conf=parse_conf(c_f)

	required_parameter=['html_description', 'mysql_password', 'project_name', 'example_Interpro_ID', 'mysql_user', 'example_FASTA', 'dom', 'db_link_path', 'mysql_host', 'webserver', 'mysql_db', 'example_keyword', 'example_GO_ID', 'hrd', 'transcripts_NT','transcripts_AA', 'fpkm_value_matrix', 'example_gene_identifier']
	required_parameter.sort()

	for required_parameter_ in required_parameter:
		assert(conf.get(required_parameter_)!=None)
		cv=conf[required_parameter_]
		if(required_parameter_!="mysql_password" and required_parameter_.find("example")==-1):
			if(len(cv)==0):
				print
				print "ERROR","parameter",required_parameter_,"is not defined"
				print 
				sys.exit(-1)

	webserver=conf["webserver"]
	if(webserver.find("http://")==-1):
		print 
		print "ERROR","parameter","webserver","has to start with http://"
		print
		sys.exit(-1)

	if(os.path.exists(conf["hrd"])==False):
	       	print
	        print "ERROR","file","hrd","does not exist"
	        print
	        sys.exit(-1)
	else:
	        fh=file(conf["hrd"])
	        for line in fh.readlines():
	                line=line.strip()
	                vals=line.split("\t")
	                if(len(vals)>2):
	                        print
	                        print "ERROR","hrd","only two values allowed seperated by a tab"
	                        print
	                        sys.exit(-1)
	        fh=file(conf["hrd"])
	        header=fh.readlines()[0]
	        header=header.strip()
		header=header.split("\t")
		if(not(header[0]=="transcript" and header[1]=="description")):
	                print
                	print "ERROR","hrd","two header need to have following names: transcript (column 1) and description(column 2)"
                	print
                	sys.exit(-1)

	if(os.path.exists(conf["dom"])==False):
	        print
	        print "ERROR","file","dom","does not exist"
	        print
		sys.exit(-1)
	else:
		fh=file(conf["dom"])
		for line in fh.readlines():
			line=line.strip()
			vals=line.split("\t")
			if(len(vals)!=2 and len(vals)==0):
				print 
				print "ERROR","dom","only two values allowed seperated by a tab"	
				print
				sys.exit(-1)
		fh=file(conf["dom"])
		header=fh.readlines()[0]
		header=header.strip()
		header=header.split("\t")
		if(not(header[0]=="transcript" and header[1]=="domain")):
			print
			print "ERROR","dom","two header need to have following names: transcript (column 1) and domain (column 2)"
			print
			sys.exit(-1)

	if(os.path.exists(conf["transcripts_NT"])==False):
	        print
	        print "ERROR","file","transcripts (for nucleotides)","does not exist"
	        print
	        sys.exit(-1)

        if(os.path.exists(conf["transcripts_AA"])==False):
                print
                print "ERROR","file","transcripts (for proteins)","does not exist"
                print
                sys.exit(-1)

        if(os.path.exists(conf["fpkm_value_matrix"])==False):
                print
                print "ERROR","file","fpkm_value_matrix","does not exist"
                print
                sys.exit(-1)

	if(os.path.exists(conf["html_description"])==False):
	        print
	        print "ERROR","file","html_description","does not exist"
	        print
	        sys.exit(-1)

	print
	print
	print "SUCCESS","check_configuration"
	print	
	print

