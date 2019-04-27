#!/usr/bin/env python3
import os
from math import *
import numpy as np
from parameter import *
from parseprogs import *
from makea import *
from scopy import *
from normlz import *


def main():
	mustv = 4
	mustf = 2


	# common area
	a = np.zeros(SIZEOFA, dtype=np.float32)
	ja = np.zeros(SIZEOFA, dtype=np.int32)
	na = np.zeros(MMAX, dtype=np.int32)
	b = np.zeros(MMAX, dtype=np.float32)
	jndx = np.zeros(NMAX, dtype=np.int32)

	u = np.zeros(MMAX, dtype=np.float32)
	v = np.zeros(NMAX, dtype=np.float32)
	w = np.zeros(MMAX, dtype=np.float32)
	x = np.zeros(NMAX, dtype=np.float32)
	se = np.zeros(NMAX, dtype=np.float32)

	m = None
	n = None
	istop = 0
	(anorm, acond, rnorm, arnorm, dampsq, xnorm) = (None, None, None, None, None, None) 
	nbl = None

	files = ["dtdsfil", "resfile", "nmodfil", "fresfil"]
	VERSION = "2004.0924"

	one = 1.0
	ione = 1

	lout = 2
	nout = None

	lunspc =   4
	lundts =  19
	lunres =  20
	lunfmd =  45
	lunfrs =  46

	# Default setting for some variables
	damper =  0.001
	# Iteration limit. if = 0, use the default iteration limit
	intlims = 0

	ittnum = 1

	# End of default values

	# the line below is for testing only, replace with the line above
	specfile = os.path.relpath("data/taiwan.nspec_sph01")
	#specfile = input(' Enter parameter specification file: ')
	lunspc = open(specfile)

	# recover the variables needed to run this program
	dtdsfil = getvars(lunspc, files[0], 1)
	resfile = getvars(lunspc, files[1], 1)
	nmodfil = getvars(lunspc, files[2], 1)
	fresfil = getvars(lunspc, files[3], 1)

	# Optionally read in some variables
	# Reading option
	damper = float(getvars(lunspc, "damper"))
	intlims = int(getvars(lunspc, "intlim"))
	ittnum = int(getvars(lunspc, "ittnum"))
	# end of optional parameters

	logfile = "data/runlsqr.log%d" % int(ittnum)
	lout = open(logfile, "w")

	lout.write(' \n')
	lout.write('***************************************************************\n')
	lout.write('         Parameters Set For This Run of Runlsqr \n')
	lout.write(' \n')
	lout.write(' runlsqr VERSION: %s\n' % VERSION)
	lout.write(' \n')
	lout.write(' Current parameter specification file: %s' % specfile)
	lout.write(' \n')
	lout.write(' Iteration counter:       %s\n' % ittnum)
	lout.write(' \n')
	lout.write('Damper: %s\n' % damper)
	lout.write('Intlim: %s\n' % intlims)
	lout.write(' \n')
	lout.write('Input file attachments:\n')
	lout.write(' \n')
	lout.write(' A matrix:                     %s\n' % dtdsfil)
	lout.write(' Data Vector:                  %s\n' % resfile)
	lout.write(' \n')
	lout.write('Output file attachments:\n')
	lout.write(' \n')
	lout.write(' Perturbations:                %s\n' % nmodfil)
	lout.write(' Residuals:                    %s\n' % fresfil)
	lout.write(' \n')
	lout.write('*************************************************************** \n')

	damp = damper

	lunfmd = open("data/" + nmodfil, "wb")
	lunfrs = open("data/" + fresfil, "w")
	lundts = open("data/" + dtdsfil, "rb")
	lunres = open("data/" + resfile, "rb")

	#######################################################################
	# generate a and b.  the vector r, ja, and na will define the matrix a.
	#######################################################################
	print(' Reading in a and b ... ')
	lout.write(' Reading in a and b ... \n')
	(m, nbl, jndx, a, na, ja, b) = makea(m, nbl, lundts, lunres, lout, jndx, a, na, ja, b)
	n = nbl
	

	########################################################################
	# solve the problem defined by aprod, damp, and b
	########################################################################
	# copy the rhs vector b into u (lsqr will overwrite u) and set the
	# other input parameters for lsqr.  change the value of damp as needed.
	scopy(m,b,1,u,1)
	# for uu in u:
	# 	if(uu!=0):
	# 		print("%.4f" % uu)

	relpr = 1e-12
	atoL = relpr
	btol = relpr
	conlim = 1/(10*sqrt(relpr))
	# This value is of intlim is appropriate for ill conditioned systems
	intlim = 4*n
	print(' Suggested intlim = ', intlim)
	lout.write(' Suggested intlim = %d\n' % intlim)

	if intlims != 0:
		intlim = intlims

	print(" least-squares test problem      p(%8d%8d  %10.6f %10.2f%8d\n" % (m, n, damp, conlim, intlim))

	lout.write(" least-squares test problem      p(%8d%8d  %10.6f %10.2f%8d\n\n" % (m, n, damp, conlim, intlim))	

	(iw, rw, u, v, w, x, se, rnorm, arnorm, xnorm) = lsqr(m, n, damp, 1, 1, ja, a, u, v, w, x, se, atoL, btol, conlim, intlim, nout, istop, anorm, acond, rnorm, arnorm, xnorm, lout, a, na, ja)

	########################################################################
	# examine the results.
	# we print the residual norms rnorm and arnorm given by lsqr,
	# and then compute their true values in terms of the solution x
	# obtained by lsqr.  at least one of them should be small.
	########################################################################

	one = 1
	ione = 1
	dampsq = damp**2

	lout.write("                  residual norm (abar*x - bbar)    residual norm (normal eqns)    solution norm (x)\n")
	lout.write("                  -----------------------------    ---------------------------    -----------------\n\n")
	lout.write(" estimated by lsqr          %.6E                   %.6E              %.6E\n" % (rnorm, arnorm, xnorm))
	print("                  residual norm (abar*x - bbar)    residual norm (normal eqns)    solution norm (x)\n")
	print("                  -----------------------------    ---------------------------    -----------------\n\n")
	print("estimated by lsqr          %.6E                   %.6E              %.6E\n" % (rnorm, arnorm, xnorm))

	# compute u = a*x 
	# Do this using aprod by setting u to zero then forming the product 
	# u <- A*x - u
	# Thus u will contain predicted travel times
	for i in range(0, m):
		u[i] = 0.

	(x, u) = aprod(1,m,n,x,u,ione,ione,iw,rw, a, na, ja)

	for i in range(0, m):
		lunfrs.write("%lf %lf %lf" % (b[i], u[i], u[i] - b[i]))

	buffer_ = np.int32(4)
	header = np.int32(15076)
	ender = np.int32(15076)


	lunfmd.write(bytes(buffer_))
	lunfmd.write(bytes(n))
	lunfmd.write(bytes(buffer_))
	lunfmd.write(bytes(header))
	lunfmd.write(bytes(x[:n]))
	lunfmd.write(bytes(ender))
	lunfmd.write(bytes(header))
	lunfmd.write(bytes(jndx[:n]))
	lunfmd.write(bytes(ender))
	lunfmd.write(bytes(header))
	lunfmd.write(bytes(se[:n]))
	lunfmd.write(bytes(ender))





def aprod(mode, m, n, x, y, leniw, lenrw, iw, rw, a, na, ja):
	

	if mode == 1:
		# set y = y + a*x.
		l1 = 0
		l2 = 0
		for i in range(0, m):
			if na[i] > 0: 
				sum = 0.
				l1 = l2
				l2 += na[i]
				for l in range(l1, l2):
					sum += a[l] * x[ja[l]]
				y[i] += sum

	elif mode == 2:
		# set x = x + a(transpose) * y
		l1 = 0
		l2 = 0
		for i in range(0, m):
			if na[i] > 0: 
				yi = y[i]
				l1 = l2
				l2 += na[i]
				for l in range(l1, l2):
					x[ja[l]] += (a[l] * yi)
	else:
		print("mode = %d is unknow\n" % mode)


	return (x, y)


def lsqr(m,n,damp,
		leniw,lenrw,iw,rw,
		u,v,w,x,se,
		atoL,btol,conlim,itnlim,nout,
		istop,anorm,acond,rnorm,arnorm,xnorm,
		lout, a, na, ja):


	#--
	def terminate_and_printinfo(itn, istop, atoL, btol):
		print(" no. of iterations =%6d         stopping condition =%3d\n\n" % (itn, istop))

		switcher = {
			0: 	" the exact solution is  x = 0.                      \n\n\n",
			1:  " a*x - b  is small enough, given  atoL=%f, btol=%f        \n\n\n" % (atoL, btol),
			2:  " the least-sqrs soln is good enough, given  atoL=%f    \n\n\n" % (atoL),
			3:  " the estimate of  cond(abar)  has exceeded  conlim  \n\n\n",
			4:  " a*x - b   is small enough for this machine\n\n\n",
			5:  " the least-sqrs soln is good enough for this machine\n\n\n",
			6:  " cond(abar)   seems to be too large for this machine\n\n\n",
			7:  " the iteration limit has been reached               \n\n\n"
		}

		error_statement = switcher.get(istop, "")
		print(error_statement)

		return
	#--





	print("%25slsqr   --   least-squares solution of  a*x = b\n\n" % "")
	print("%25sthe matrix  a  has %8d rows   and %8d cols\n" % ("", m, n))
	print("%25sthe damping parameter is    damp   = %4.2E\n\n" % ("", damp))
	print("%25satoL   =%10.2E          conlim =%10.2E\n" % ("", atoL, conlim))
	print("%25sbtol   =%10.2E          itnlim =%10d\n" % ("", btol, itnlim))
	
	lout.write("%25slsqr   --   least-squares solution of  a*x = b\n\n" % "")
	lout.write("%25sthe matrix  a  has %8d rows   and %8d cols\n" % ("", m, n))
	lout.write("%25sthe damping parameter is    damp   = %4.2E\n\n" % ("", damp))
	lout.write("%25satoL   =%10.2E          conlim =%10.2E\n" % ("", atoL, conlim))
	lout.write("%25sbtol   =%10.2E          itnlim =%10d\n" % ("", btol, itnlim))

	ctol = 0
	if conlim > 0:
		ctol = 1 / conlim
	
	dampsq = damp * damp

	
	anorm = 0
	acond = 0
	bbnorm = 0
	ddnorm = 0
	res2 = 0
	xnorm = 0
	xxnorm = 0
	cs2 = -1
	sn2 = 0
	z = 0
	itn = 0
	istop = 0
	nstop = 0

	for i in range(0,n): 
		v[i] = 0
		x[i] = 0
		se[i] = 0
	
	# set up the first vectors for the bidiagonalization.
	# these satisfy   beta*u = b,   alfa*v = a(transpose)*u.
	beta = 0
	
	# print("m :", m)
	# for xx in u:

	# 	print("%.4f" % xx)
	# 	if(xx==0):
	# 		break

	beta = normlz(m, u, beta)
	(v, u) = aprod(2, m, n, v, u, leniw, lenrw, iw, rw, a, na, ja)
	alfa = 0
	alfa = normlz(n, v, alfa)
	scopy(n, v, 1, w, 1)

	rhobar = alfa
	phibar = beta
	bnorm = beta
	rnorm = beta
	arnorm = alfa * beta
	
	

	if arnorm <= 0:
		terminate_and_printinfo(itn, istop, atoL, btol)
		return (iw, rw, u, v, w, x, se, rnorm, arnorm, xnorm)

	if nout == None:
		if dampsq <= 0:
			print("   itn         x(1)              function       compatible incompatible norm(a) cond(a)\n\n")
		else:
			print("   itn         x(1)                 function       compatible incompatible norm(abar) cond(abar)\n\n")
			
		test1 = 1
		test2 = alfa / beta
		print("%5d    %.12E   %.12E    %.3E     %.2E\n\n" % (itn, x[0], rnorm, test1, test2))
	

#   ------------------------------------------------------------------
#   start of iteration loop.
#   ------------------------------------------------------------------

	while(True):

		itn += 1
	#      perform the next step of the bidiagonalization to obtain the
	#      next  beta, u, alfa, v.  these satisfy the relations
	#                 beta*u  =  a*v  -  alfa*u,
	#                 alfa*v  =  a(transpose)*u  -  beta*v.
	#
		sscal(m, (-alfa), u, 1)
		(v, u) = aprod(1, m, n, v, u, leniw, lenrw, iw, rw, a, na, ja)
		beta = normlz(m, u, beta)
		bbnorm = bbnorm + alfa * alfa + beta * beta + dampsq
		sscal(n, (-beta), v, 1)
		(v, u) = aprod(2, m, n, v, u, leniw, lenrw, iw, rw, a, na, ja)
		alfa = normlz(n, v, alfa)

	#     use a plane rotation to eliminate the damping parameter.
	#     this alters the diagonal (rhobar) of the lower-bidiagonal matrix.
		rhbar2 = rhobar * rhobar + dampsq
		rhbar1 = sqrt(rhbar2)
		cs1 = rhobar / rhbar1
		sn1 = damp / rhbar1
		psi = sn1 * phibar
		phibar = cs1 * phibar

	#      use a plane rotation to eliminate the subdiagonal element (beta)
	#      of the lower-bidiagonal matrix, giving an upper-bidiagonal matrix.

		rho = sqrt(rhbar2 + beta * beta)
		cs = rhbar1 / rho
		sn = beta / rho
		theta = sn * alfa
		rhobar = -cs * alfa
		phi = cs * phibar
		phibar = sn * phibar
		tau = sn * phi

	#     update  x, w  and the standard error estimates.
		t1 = phi / rho
		t2 = -theta / rho
		t3 = 1 / rho
		for i in range(0, n):
			t = w[i]
			x[i] += t1 * t
			w[i] = t1 * t + v[i]
			t = (t3 * t) * (t3 * t)
			se[i] += t
			ddnorm += t
		

	#     use a plane rotation on the right to eliminate the
	#     super-diagonal element (theta) of the upper-bidiagonal matrix.
	#     then use the result to estimate  norm(x).

		delta = sn2 * rho
		gambar = -cs2 * rho
		rhs = phi - delta * z
		zbar = rhs / gambar
		xnorm = sqrt(xxnorm + zbar * zbar)
		gamma = sqrt(gambar * gambar + theta * theta)
		cs2 = gambar / gamma
		sn2 = theta / gamma
		z = rhs / gamma
		xxnorm = xxnorm + z * z

	#      test for convergence.
	#      first, estimate the norm and condition of the matrix  abar,
	#      and the norms of  rbar  and  abar(transpose)*rbar.

		anorm = sqrt(bbnorm)
		acond = anorm * sqrt(ddnorm)
		res1 = phibar * phibar
		res2 = res2 + psi * psi
		rnorm = sqrt(res1 + res2)
		arnorm = alfa * fabs(tau)

	#      now use these norms to estimate certain other quantities,
	#      some of which will be small near a solution.

		test1 = rnorm / bnorm
		test2 = arnorm / (anorm * rnorm)
		test3 = 1 / acond
		t1 = test1 / (1 + anorm * xnorm / bnorm)
		rtol = btol + atoL * anorm * xnorm / bnorm

	#      the following tests guard against extremely small values of
	#      atoL, btol  or  ctol.  (the user may have set any or all of
	#      the parameters  atoL, btol, conlim  to zero.)
	#      the effect is equivalent to the normal tests using
	#      atoL = relpr,  btol = relpr,  conlim = 1/relpr.

		t3 = 1 + test3
		t2 = 1 + test2
		t1 = 1 + t1

	
		if itn >= itnlim:
			istop = 7
		if round(t3, 7) <= 1:
			istop = 6
		if round(t2, 7) <= 1:
			istop = 5
		if round(t1, 7) <= 1:
			istop = 4

	#      allow for tolerances set by the user.

		if test3 <= ctol:
			istop = 3
		if test2 <= atoL:
			istop = 2
		if test1 <= rtol:
			istop = 1
	#     ==================================================================
	#     see if it is time to print something.
	#     ==================================================================
		if ((m <= 40 or n <= 40) or (itn <= 10) or (itn >= itnlim - 10)
				or (itn % 10 == 0) or (test3 <= 2.0 * ctol)
				or (test2 <= 10.0 * atoL) or (test1 <= 10.0 * rtol)):
			
			print("%5d    %.12E   %.12E    %.3E     %.2E   %.2E   %.2E\n" % (itn,x[0],rnorm,test1,test2, anorm, acond))
			
		
	#     print a line for this iteration.
	#       ==================================================================
	#
	#      stop if appropriate.
	#      the convergence criteria are required to be met on  nconv
	#      consecutive iterations, where  nconv  is set below.
	#      suggested value --   nconv = 1, 2  or  3.
		
		if istop == 0:
			nstop = 0
		if istop == 0:
			continue
		nconv = 1
		nstop += 1
		if (nstop < nconv and itn < itnlim):
			istop = 0

		if istop == 0:
			continue

		# if the conditions are not met then break loop 	
		break

#   ------------------------------------------------------------------
#   end of iteration loop.
#   ------------------------------------------------------------------



#      finish off the standard error estimates.


	t = 1
	if m > n:
		t = m - n
	if dampsq > 0:
		t = m
	t = rnorm / sqrt(t)

	for i in range(0, n):
		se[i] = t * sqrt(se[i])
	
	
	terminate_and_printinfo(itn, istop, atoL, btol)
	return (iw, rw, u, v, w, x, se, rnorm, arnorm, xnorm)



main()