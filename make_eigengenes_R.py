import sys

tmp=sys.argv[1]

a="""
require(WGCNA)
library(gplots)
library(RColorBrewer)
# ----------------------
o1=5
o2=5
o3=0
o4=50
w1=15
h1=8
LEGEND_LIM=5
# ----------------------
finalGrid <- function(nx, ny,col="lightgrey"){
  grid(nx=nx, ny=ny, col=col, lty=1, lwd=1)
  box()
}
# ----------------------
genotype.colos <- brewer.pal(5, "Set1")
names(genotype.colos) <- paste0("C",c("M",1:4))
genotype.colos[["Remus"]]="lightgrey"
assign("genotype.colos",genotype.colos,1)

data=read.csv("XXTEMP/EIGENGENES_INPUT",sep="\\t",header=T,row.names=1)
m0=as.matrix(data[,1:(dim(data)[2])])
m0=m0[!apply(m0==0,1,all),]
m0=log2(m0+1)
if(!is.null(dim(m0))){
        m=t(apply(m0,1,scale))
}else{
        m=scale(m0)
        m=matrix(m,ncol=length(m))
}
rownames(m)=rownames(m0)
colnames(m)=gsub("_FPKM","",colnames(m0))
m0
colN=colnames(m)
mybreaks=seq(-LEGEND_LIM,LEGEND_LIM,length.out=100)

pdf("XXTEMP/EIGENGENES_test.pdf",width=w1,height=h1)
par(oma=c(o1,o2,o3,o4/3),las=2)
ME=moduleEigengenes(t(m),colors=rep('blue',nrow(m)))
rownames(ME$eigengenes) <- colnames(m)
barplot(ME$eigengenes[,1],col=genotype.colos[gsub("[MF][35]0","",rownames(ME$eigengenes))],names=rownames(ME$eigengenes), main=sprintf("n=%s", nrow(m)))
dev.off()

pdf("XXTEMP/EIGENGENES_test_hm.pdf",width=w1,height=h1)
if(dim(data)[1]<2){
        par(oma=c(o1,o2,o3,o4/2))
        barplot(m,names=colN,las=2,main=data[1,1])
}else{
        par(oma=c(o1,o2,o3,o4))
        #heatmap.2(m,trace="none",col=colorRampPalette(c("blue","white","red"))(length(mybreaks)-1),dendrogram = "none", Rowv = TRUE, Colv = FALSE,breaks=mybreaks,colsep=c(4,8,12,16), sepcolor="black")
        heatmap.2(m, scale="n", trace="none", density.info="n",dendro="row", Colv=FALSE, main="", breaks=mybreaks, col=colorRampPalette(c("blue","white","red"))(length(mybreaks)-1), add.expr={finalGrid(ncol(m), nrow(m))}, ColSideColors=genotype.colos[gsub("[MF][35]0","",colnames(m))], cexRow=0.5, colsep=c(4,8,12), sepcolor="black", cex.main=0.5)
}
dev.off()
pdf("XXTEMP/EIGENGENES_test_bx.pdf",width=w1,height=h1)
data=read.csv("XXTEMP/EIGENGENES_INPUT2",sep="\\t",header=F)
barplot(data[,2],names=data[,1],las=2)
dev.off()
"""
a=a.replace("XXTEMP",tmp)

print a

