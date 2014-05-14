local_grad3
access: linearize
defines:
	lx = 10
	ly = 10
	lz = 10
	nelt = 100
input:
	us:(nelt,lx,ly,lx)
	ut:(nelt,lx,ly*lz)
	D:(lx,ly)
	Dt:(lx,ly)
output:
	w1:(nelt,lx,ly,lz)
	w:(nelt,lx,ly*lz)
operation:
	w1:(e,j,i,k) += us:(e,j,m,k)*Dt:(i,m)
	w:(e,j,i) += ut:(e,k,i)*Dt:(j,k)
