local_grad3
access: linearize
defines:
	N = 10
input:
	u:(N,N)
	B:(N,N)
	A:(N,N)
output:
	C:(N,N)
io:
	w:(N,N)
operation:
	w:(i,j) += u:(i,k)*B:(k,j)
	C:(i,j) += A:(i,k)*w:(k,j)
