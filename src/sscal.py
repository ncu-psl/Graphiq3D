def sscal(n, sa, sx, incx):
# replace single precision sx by single precision sa*sx.
# for i = 0 to n-1, replace sx(1+i*incx) with  sa * sx(1+i*incx)
	if (n <= 0):
		return
	if (incx == 1):
		m = n % 5
		if (m != 0):
			for i in range(0, m):
				sx[i] *= sa
			
			if (n < 5) :
				return

		mp1 = m
		for i in range(mp1, n, 5):
			for j in range(0, 5):
				sx[i + j] *= sa

	else:
# ode for increments not equal to 1.
		ns = n * incx
		for i in range(0, ns, incx):
			sx[i] *= sa
