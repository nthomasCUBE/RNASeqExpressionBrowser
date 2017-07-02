import sys

cuffdiff_outdir=sys.argv[1]

fh=file(cuffdiff_outdir+"/"+"genes.fpkm_tracking")
for line in fh.readlines():
	line=line.strip()
	line=line.replace("tracking","transcript")
	line=line.replace("gene_id","gene")
	vals=line.split()
	if(vals[3]!="-"):
		print vals[0],vals[3],
		for x in range(9,len(vals),4):
			print vals[x],
		print
		

