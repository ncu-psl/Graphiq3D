from snrm2 import *
from sscal import *

# return beta
def normlz(n, x,  beta):
#      normlz  is required by subroutine lsqr.  it computes the
#      euclidean norm of  x  and returns the value in  beta.
#      if  x  is nonzero, it is scaled so that norm(x) = 1.
#
#      functions and subroutines
#
#      blas       snrm2,sscal
	

	beta = snrm2(n, x, 1)


	if (beta > 0):
		sscal(n, 1 / beta, x, 1)

			
	
	return beta
