c_std_s1_1
access: linearize
memory: column
pattern: strided
defines:
	tilesize = 16
input:
	T1:(tilesize,tilesize)
	v2:(tilesize,tilesize,tilesize,tilesize)
output:
	T3:(tilesize,tilesize,tilesize,tilesize,tilesize,tilesize)
operation:
	T3:(h3,h2,h1,p6,p5,p4) += T1:(p4,h1)*v2:(h3,h2,p6,p5)
