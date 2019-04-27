import math
from goto import with_goto

@with_goto
def snrm2(n, sx, incx):
	cutlo = 4.441e-16
	cuthi = 1.304e19

	

	# integer
	i = 0
	j = 0
	next_ = 0
	nn = 0

	#float
	hitest = 0
	sum_ = 0
	xmax = 0
	snrm_2 = 0
	
	if (n > 0):
		goto .a10
	goto .a300

	label .a10
	next_ = 30
	sum_ = 0
	nn = n * incx
	i = 0

	label .a20
	if (next_ == 30):
		goto .a30
	if (next_ == 50):
		goto .a50
	if (next_ == 70):
		goto .a70
	if (next_ == 110):
		goto .a110

	label .a30
	if (math.fabs(sx[i]) > cutlo):
		goto .a85
	next_ = 50
	xmax = 0

	label .a50
	if (sx[i] < 0.0001): #as zero
		goto .a200
	if (math.fabs(sx[i]) > cutlo):
		goto .a85
	next_ = 70
	goto .a105

	label .a100
	i = j
	next_ = 110
	
	sum_ = sum_ / sx[i] / sx[i]
	

	label .a105
	xmax = math.fabs(sx[i])
	goto .a115

	label .a70
	if (math.fabs(sx[i]) > cutlo):
		goto .a75

	label .a110
	if (math.fabs(sx[i]) <= xmax):
		goto .a115
	sum_ = 1 + sum_ * (xmax / sx[i]) * (xmax / sx[i])
	
	xmax = math.fabs(sx[i])
	goto .a200

	label .a115
	sum_ += (sx[i] / xmax) * (sx[i] / xmax)
	
	goto .a200

	label .a75
	sum_ = sum_ * xmax * xmax

	label .a85
	hitest = cuthi / n
	for j in range(i, nn, incx):
		if (math.fabs(sx[j]) >= hitest):
			goto .a100
		sum_ += sx[j] * sx[j]
	
	snrm_2 = math.sqrt(sum_)
	
	goto .a300

	label .a200
	i += incx
	if (i <= nn):
		goto .a20
	snrm_2 = xmax * math.sqrt(sum_)
	label .a300 #do nothing

	return snrm_2