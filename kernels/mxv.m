mxm
access: multidimension
memory: row
pattern: strided
define:
	N = 1024
variables:
	a:order2
	b:order1
	c:order1
operations:
	c:(i) += a:(i,k) * b:(k)

