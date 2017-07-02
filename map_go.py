import string

fh=file("go_mapping.txt")

lines=fh.readlines()

a=(lines[0]).strip()
b=(lines[1]).strip()

a=(a.split("\t"))
b=(b.split("\t"))

for x in range(0,len(b)):
	if(x<len(a) and x<len(b)):
		if(b[x]!="NA"):
			v=a[x]
			v=v.replace("\"","")
			r=b[x]
			r=r.replace("c(","")
			r=r.replace(",","")
			r=r.replace(")","")
			r=r.replace("\"","")
			r=r.split()
			r=string.join(r,";")+";"
			print v,r
		
