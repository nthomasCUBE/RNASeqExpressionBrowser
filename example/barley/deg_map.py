print "gene\tcomparison"

mm={}

fh=file("fpkm.TXT")
i=0
for line in fh.readlines():
	line=line.strip()
	vals=line.split()
	i=i+1
	if(i==1):
		h=vals
	else:
		for x in range(2,len(vals)):
			if(mm.get(vals[0])==None):
				mm[vals[0]]={}
			mm[vals[0]][h[x]]=float(vals[x])
			
allH=h[2:]
allH.sort()

nn={}

for mm_ in mm:
	for x in range(0,len(allH)):
		for y in range(0,len(allH)):
			if(x!=y):
				if(str(allH[x])>str(allH[y])):
					c_cmp=allH[x]+"_vs_"+allH[y]+"log2_change_gt_2"	
					if(float(mm[mm_][allH[x]])/(float(mm[mm_][allH[y]])+0.00001)>=4):
						if(nn.get(c_cmp)==None):
							nn[c_cmp]={}
						nn[c_cmp][mm_]=1



for nn_ in nn:
	LL=nn[nn_]
	for LL_ in LL:
		print LL_+"\t"+nn_
	
