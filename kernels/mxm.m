mxm
define:
	N = 1024
variables:
	a:(N,N)
	b:(N,N)
	c:(N,N)
operations:
	c:(i,j) += a:(i,k) * b:(k,j)

