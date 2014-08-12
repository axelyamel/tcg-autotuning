local_grad3
access: linearize
define:
	lx = 10
	ly = 10
	lz = 10
	nelt = 100
variables:
	u:(nelt,lx,ly,lz)
	D:(lx,ly)
	Dt:(lx,ly)
	ur:(nelt,lx*ly,lz)
	us:(nelt,lx,ly,lx)
	ut:(nelt,lx,ly*lz)
operations:
	ur:(e,j,i) += D:(k,i)*u:(e,j,k)
	us:(e,j,i,k) += u:(e,j,m,k)*Dt:(i,m)
	ut:(e,j,i) += u:(e,k,i)*Dt:(j,k)
