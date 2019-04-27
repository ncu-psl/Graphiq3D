def scopy(n, sx, incx, sy, incy):
#    copy single precision sx to single precision sy.
#    for i = 0 to n-1, copy  sx(lx+i*incx) to sy(ly+i*incy),
#    where lx = 1 if incx  >=  0, else lx = (-incx)*n, and ly is
#    defined in a similar way using incy.
	m = 0

	if n <= 0:
		return
	if incx == incy:
		if incx < 1:
			ix = 0
			iy = 0
			if incx < 0:
				ix = (-n + 1) * incx
			if incy < 0:
				iy = (-n + 1) * incy
			for i in range(0, n): 
				sy[iy] = sx[ix]
				ix += incx
				iy += incy
			
			return


		elif incx == 1:
			
			m = n % 7
			if m == 0:

				mp1 = m
				for i in range(mp1, n, 7): 
					for j in range(0, 7):
						sy[i + j] = sx[i + j]
				
				return


			for i in range(0, m):
				sy[i] = sx[i]
			
			if n < 7:
				return

			mp1 = m
			for i in range(mp1, n, 7): 
				for j in range(0, 7):
					sy[i + j] = sx[i + j]
			
			return

		
		else:
			ns = n * incx
			for i in range(0, ns, incx):
				sy[i] = sx[i]
			
			return
	

	
	