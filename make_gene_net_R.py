import sys

TEMP=sys.argv[1]

a="""
pdf("XXTEMP/NETWORK.pdf")

library("GeneNet")

input=read.csv(XXTEMP+"/EIGENGENES_INPUT",sep="\\t",header=T)
dim(input)
m=t(input[,4:dim(input)[2]])
x=input[,3]
names(x)=input[,1]
colnames(m)=input[,1]
pcor.dyn <- ggm.estimate.pcor(m, method = "dynamic")
arth.edges <- network.test.edges(pcor.dyn,direct=TRUE,plot=FALSE)
FILT=50
if(length(arth.edges)<50){
	FILT=length(arth.edges)
}
arth.net <- extract.network(arth.edges, method.ggm="number", cutoff.ggm=FILT)
node.labels <- colnames(m) 
igr <- network.make.igraph(arth.net, node.labels)
V(igr)$color=as.character(x[V(igr)])

plot(igr, main="Gene Set Network using R-package GeneNet", layout=layout.fruchterman.reingold,
 edge.arrow.size=0.5, vertex.size=9, vertex.label.cex=0.5)
dev.off()
"""
a=a.replace("XXTEMP",TEMP)

print a

