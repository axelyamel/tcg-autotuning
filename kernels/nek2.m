local_grad3
memory: column
access: linearize
defines:
	lx = 10
	ly = 10
	lz = 10
	nelt = 100
input:
	u:(lx,ly,lz,nelt)
	u1:(lz,lx*ly,nelt)
	u2:(ly*lz,lx,nelt)
	D:(lx,ly)
	Dt:(lx,ly)
output:
	ur:(lz,lx*ly,nelt)
	us:(lx,ly,lz,nelt)
	ut:(ly*lz,lx,nelt)
operation:
	ur:(i,j,e) += D:(k,i)*u1:(j,k,e)
	us:(k,i,j,e) += u:(m,k,j,e)*Dt:(i,m)
	ut:(i,j,e) += u2:(k,i,e)*Dt:(j,k)
