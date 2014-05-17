local_grad3
access: linearize
define:
	N = 10
variables:
      u:(N,N)
	B:(N,N)
	A:(N,N)
	C:(N,N)
	w:(N,N)
operations:
 w:(i,j)+=u:(i,k)*B:(k,j)
	C:(i,j) += A:(i,k)*w:(k,j)
