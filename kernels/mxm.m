mxm
define:
	N = 1024
variables:
	a:order2
	b:order2
	c:order2
operations:
	c:(i,j) += a:(i,k) * b:(k,j)

