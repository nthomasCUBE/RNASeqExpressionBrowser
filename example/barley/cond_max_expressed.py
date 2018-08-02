import sys

fh=file("fpkm.TXT")
i=0
mm={}
for line in fh.readlines():
	line=line.strip()
	vals=line.split()
	i=i+1
	if(i>1):
		c_h=None
		c_v=-1
		for x in range(2,len(vals)):
			if(float(vals[x])>c_v):
				c_v=float(vals[x])
				c_h=h[x]
		if(mm.get(c_h)==None):
			mm[c_h]=[]
		mm[c_h].append(vals)
	else:
		h=vals

unique={}
print "gene\tmodule\tisHub"
for mm_ in mm:
	gg=mm[mm_]
	for gg_ in gg:
		if(unique.get(gg_[0])==None):
			print str(gg_[0])+"\t"+mm_+"\t"+"TRUE"
		unique[gg_[0]]=1
