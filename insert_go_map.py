import os
import sys

RSCRIPT="""
options(stringsAsFactors=FALSE)
library("GO.db")
data=read.csv("XXX_INPUT",sep="\\t",header=F)
ids=data[,1]
i=0
write.table(cbind("GO_term","GO_term_offsprings","GO_term_parents"),append=FALSE,file="go_stats_plugin.TXT",sep="\t",col.names=F)
for(x in 1:length(ids)){
        i=i+1
        print(i)
        if(exists(ids[x],where=GOMFOFFSPRING)){
                offspring1=GOMFOFFSPRING[ids[x]]
                offspring1=(as.list(offspring1))
                offspring1=lapply(offspring1,unlist)[[1]]
        }else{
                offspring1=NA
        }
        if(exists(ids[x],where=GOBPOFFSPRING)){
                offspring2=GOBPOFFSPRING[ids[x]]
                offspring2=(as.list(offspring2))
                offspring2=lapply(offspring2,unlist)[[1]]
        }else{
                offspring2=NA
        }
        if(exists(ids[x],where=GOMFPARENTS)){
                parents1=GOMFPARENTS[ids[x]]
                parents1=(as.list(parents1))
                parents1=lapply(parents1,unlist)[[1]]
        }else{
                parents1=NA
        }
        if(exists(ids[x],where=GOBPPARENTS)){
                parents2=GOBPPARENTS[ids[x]]
                parents2=(as.list(parents2))
                parents2=lapply(parents2,unlist)[[1]]
        }else{
                parents2=NA
        }
        offspring=c(offspring1,offspring2)
        parents=c(parents1,parents2)

        offspring=offspring[!is.na(offspring)]
        parents=parents[!is.na(parents)]

        offspring=paste(as.list(offspring),collapse=";")
        parents=paste(as.list(parents),collapse=";")
        write.table(cbind(ids[x],offspring,parents),append=TRUE,file="go_stats_plugin.TXT",sep="\t",col.names=F)

}
"""

#       ------------------------------------------------------------------------------------

ORIGIN="example/dattel2/domain.TXT"
fh=file(ORIGIN)
GO={}
for line in fh.readlines():
	line=line.strip()
	vals=line.split()
	if(vals[1].find("GO:")!=-1):
		GO[vals[1]]=1
fw=file("insert_go_map_INPUT","w")
for GO_ in GO:
	fw.write(GO_+"\n")
fw.close()
_RSCRIPT=RSCRIPT.replace("XXX_INPUT","insert_go_map_INPUT")
fw=file("insert_go_map.R","w")
fw.write(_RSCRIPT)
fw.close()
os.system("/tmp/R-3.1.2/bin/R -f insert_go_map.R")

#	------------------------------------------------------------------------------------

fh=file("go_stats_plugin.TXT")
GO={}
i=0
for line in fh.readlines():
	line=line.strip()
	line=line.replace("\"","")
	vals=line.split("\t")
	i=i+1
	if(i>1):
		GO[vals[1]]=1
		child=vals[2].split(";")
		for child_ in child:
			if(child_.find("NA")==-1):
				GO[child_]=1
		parents=vals[3].split(";")
		for parents_ in parents:
			if(parents_.find("NA")==-1):
				GO[parents_]=1
fw=file("insert_go_map_INPUT","w")
for GO_ in GO:
        fw.write(GO_+"\n")
fw.close()
_RSCRIPT=RSCRIPT.replace("XXX_INPUT","insert_go_map_INPUT")
fw=file("insert_go_map.R","w")
fw.write(_RSCRIPT)
fw.close()
os.system("/tmp/R-3.1.2/bin/R -f insert_go_map.R")

#       ------------------------------------------------------------------------------------

fw=file("sql.imports.TXT","w")
fw.write("DROP TABLE test4.dattelGO2;"+"\n")
fw.write("CREATE TABLE test4.dattelGO2 (go_id VARCHAR(50),go_offspring VARCHAR(20000),PRIMARY KEY(go_id)) ENGINE=MyISAM;"+"\n")
fh=file("go_stats_plugin.TXT")
i=0
for line in fh.readlines():
	line=line.strip()
	line=line.replace("\"","")
	vals=line.split("\t")
	i=i+1
	if(i>1):
		if(vals[2]!="NA"):
			fw.write("INSERT INTO test4.dattelGO2 VALUES ('"+vals[1]+"','"+vals[2]+"');"+"\n")
fw.close()

os.system("mysql --quick --user root < sql.imports.TXT")

#       ------------------------------------------------------------------------------------

