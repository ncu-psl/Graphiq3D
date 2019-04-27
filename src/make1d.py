#!/usr/bin/env python3
import os
import c2f
from parameter import *
from gridspec import *
from parseprogs import *
from math import *
import numpy as np
import binascii
import codecs

def main():
	MAX1D=1000

	mustv = 4
	mustf = 2

	nhbyte = 58

	# common area
	gx = []
	gy = []
	gz = []

	vp = []
	z = []

	head = ttype = syst = quant = flatten = \
	hcomm = fxs = fys = fzs = clat = clon = cz = \
	axo = ayo = azo = dx = dy = dz = az = nxh = nyh = nzh = None
	# --------

	vsave = np.zeros(nxyzcm2, dtype=np.float32)
	terp = []

	mvals = ["nxc", "nyc", "nzc", "h"]
	files = ["oldvfil", "onedfil"]
	rearth, degrad, hpi = 6371.0, 0.017453292, 1.570796
	VERSION = "2004.0909"

	lenhead = nhbyte*4


	# open log file part 



	# -----^ need finish


	# Default setting for some variables
	x0 = 0.
	y0 = 0.
	z0 = 0.

	df = 0.
	dq = 0.

	vs1d = 1
	iflat = 0
	isph = 0

	# fxs, fys, and fzs are not used in wavespeed models, so just set to zero
	fxs = 0.0
	fys = 0.0
	fzs = 0.0

	# End of default values


	

	# the line below is for testing only, replace with the line above
	specfile = os.path.relpath("FDtomo.spec")
	#specfile = input(' Enter parameter specification file: ')
	logfile = os.path.relpath("./data/make1d.log")
	lunspc = open(specfile)
	lout = open(logfile, 'w')

	#### Recover the variables (must) needed to run this program
	#
	#       nxc, nyc, ggnzc      coarse dimensions of the fine mesh used in the trt tables
	#       h                  fine grid spacing
	#

	nxc = int(getvars(lunspc, mvals[0], 1))
	nyc = int(getvars(lunspc, mvals[1], 1))
	nzc = int(getvars(lunspc, mvals[2], 1))
	h = float(getvars(lunspc, mvals[3], 1))
	oldvfil = getvars(lunspc, files[0], 1)
	onedfil = getvars(lunspc, files[1], 1)

	# dimension check
	if nxc > nxcm:
		print(' nxc is too large, maximum is: ', nxcm)
		exit()
	if nyc > nycm:
		print(' nyc is too large, maximum is: ', nycm)
		exit()
	if nzc > nzcm:
		print(' nzc is too large, maximum is: ', nzcm)
		exit()

	#### Optionally read in some variables

	# Coordinate origin (used in header)
	x0 = float(getvars(lunspc, "x0"))
	y0 = float(getvars(lunspc, "y0"))
	z0 = float(getvars(lunspc, "z0"))
	clat = float(getvars(lunspc, "clat"))
	clon = float(getvars(lunspc, "clon"))
	cz = getvars(lunspc, "cz")
	az = getvars(lunspc, "az")
	df = float(getvars(lunspc, "df"))
	dq = float(getvars(lunspc, "dq"))
	# flatness, Vs, and sph  flags
	iflat = int(getvars(lunspc, "flat"))
	vs1d = int(getvars(lunspc, "vs1d")) or vs1d
	isph = int(getvars(lunspc, "sph"))

	# Grid specs
	_igridx = [int(x) for x in getvars(lunspc, "igridx")]
	_igridy = [int(x) for x in getvars(lunspc, "igridy")]
	_igridz = [int(x) for x in getvars(lunspc, "igridz")]
	igridx = np.array(_igridx, dtype=np.int32)
	igridy = np.array(_igridy, dtype=np.int32)
	igridz = np.array(_igridz, dtype=np.int32)

	#### End of optional parameters

	nxyc = nxc*nyc
	nxyzc = nxyc*nzc
	nxyzc2 = nxyzc*2

	if isph == 1:
		y00 = y0*degrad
	#	y00 = hpi - glat(y00)
		z0r = None
		y00 = hpi - glath(y00, z0, z0r)

		# If dq and df have not been specified, then make them so that the
		# interval at the surface is equal to h
		if dq == 0:  
			dq = h/rearth
		if df == 0:
			df = fabs(h/(rearth*sin(y00)))
		dy = dq/degrad
		dx = df/degrad
		

	else:
		  dx = h
		  dy = h

	nx = 1
	ny = 1
	nz = 1

	gx.append(x0)
	gy.append(y0)
	gz.append(z0)

	for i in range(1, nxc):
		nx = nx + igridx[i-1]
		gx.append(gx[i-1] + dx*igridx[i-1])
	for i in range(1, nyc):
		ny = ny + igridy[i-1]
		gy.append(gy[i-1] + dy*igridy[i-1])
	for i in range(1, nzc):
		nz = nz + igridz[i-1]
		gz.append(gz[i-1] + h*igridz[i-1])

	nxy = nx*ny
	nxyz = nxy*nz

	# dimension check
	if nx > nxm:
		print(' nx is too large, maximum is: ', nxm)
	if ny > nym:
		print(' ny is too large, maximum is: ', nym)
	if nz > nzm:
		print(' nz is too large, maximum is: ', nzm)

	lengrd = 4*(nxc + nyc + nzc - 3)
	lenrec = lenhead + lengrd + 4*nxyzc2



	lout.write(' \n')
	lout.write('*************************************************************** \n')
	lout.write('         Parameters Set For This Run of make1d.f\n')
	lout.write(' \n')
	lout.write(' VERSION:  %s\n'% VERSION)
	lout.write(' \n')
	lout.write(' Current parameter specification file:  %s\n'% specfile)
	lout.write(' \n')
	lout.write(' Latitude origin  (clat):    %.16lf\n' % clat)
	lout.write(' Longitude origin (clon):    %.16lf\n' % clon)
	lout.write(' Depth of  origin (cz)  :    %.16lf\n' % cz)
	lout.write(' Clockwise rotation (az):    %.16lf\n' % az)
	lout.write(' \n')
	lout.write(' Cartesian X origin (x0):    %.16lf\n' % x0)
	lout.write(' Cartesian Y origin (y0):    %.16lf\n' % y0)
	lout.write(' Cartesian Z origin (z0):    %.16lf\n' % z0)
	if isph == 0:
	  lout.write(' Coordinate system is CARTESIAN \n')
	  lout.write(' Fine grid spacing:  %s\n'% str(h))
	else:
	  lout.write(' Coordinate system is SPHERICAL \n')
	  lout.write(' Fine Longitude spacing (df):    %.16E\n' % dx)
	  lout.write(' Fine Latidtude spacing (dq):    %.16E\n' % dy)
	  lout.write(' Fine Radial spacing    (dz):    %s\n'% str(h))

	lout.write('\n')
	lout.write(' Number of X coarse grid nodes:       %s\n'% str(nxc))
	lout.write(' X coarse grid node spacing: \n')
	for i in range(0, nxc-1):
		lout.write(str(igridx[i])+'   ')
		if i%10 == 9:
			lout.write('\n')

	lout.write('\n')
	lout.write(' Number of Y coarse grid nodes:       %s\n'% str(nyc))
	lout.write(' Y coarse grid node spacing: \n')
	for i in range(0, nyc-1):
		lout.write(str(igridy[i])+'   ')
		if i%10 == 9:
			lout.write('\n')

	lout.write('\n')
	lout.write(' Number of Z coarse grid nodes:       %s\n'% str(nzc))
	lout.write(' Z coarse grid node spacing: \n')
	for i in range(0, nzc-1):
		lout.write(str(igridz[i])+'   ')
		if i%10 == 9:
			lout.write('\n')

	lout.write('\n')
	lout.write(' Number of X fine grid nodes:  %s\n'% str(nx))
	lout.write(' Number of Y fine grid nodes:  %s\n'% str(ny))
	lout.write(' Number of Z fine grid nodes:  %s\n'% str(nz))
	lout.write('\n')
	lout.write(' Total Number of coarse grid nodes:  %s\n'% str(nxyzc))
	lout.write(' Total Number of fine grid nodes:  %s\n'% str(nxyz))
	lout.write('\n')
	if iflat == 1:
	  lout.write(' Speeds and Depths are flattened (iflat = 1) \n')
	else:
	  lout.write(' Speeds and Depths are not flattened (iflat = 0) \n')

	if vs1d == 1:
	  lout.write(' Vs column treated as S wavespeed (vs1d = 1) \n')
	else:
	  lout.write(' Vs column treated as Vp/Vs (vs1d = 0) \n')


	lout.write('\n')

	lout.write(' Length of header  (bytes):  %s\n'% str(lenhead + lengrd))
	lout.write(' Length of outfile (bytes):  %s\n'% str(lenrec))

	lout.write('\n')
	lout.write('Input file attachments:\n')
	lout.write('\n')
	lout.write(' One-D ASCII model file:  %s\n'% str(onedfil))
	lout.write('\n')
	lout.write('Output file attachments:\n')
	lout.write('\n')
	lout.write(' New Wavespeed model file:  %s\n'% str(oldvfil))
	lout.write('\n')

	# generate the header
	head = "HEAD"
	ttype = "CORS"
	if isph == 1:
	  syst = "SPHR"
	  dx = df/degrad
	  dy = dq/degrad
	else:
	  syst = "CART"
	  dx = h
	  dy = h

	quant = "BMOD"
	if iflat == 1:
	  flatten = "FLAT"
	else:
	  flatten = "NOFL"

	hcomm = "Output from make1d.f using %s" % onedfil

	axo = x0
	ayo = y0
	azo = z0
	dz = h
	nxh = nxc
	nyh = nyc
	nzh = nzc

	# unflatten the depths if required
	# if iflat == 1:
	# 	for i = range(0, nzc)
	# 		gz[i] = uflatz(gz[i])

	file_path = os.path.relpath("TW_m30_mdl")
	lunone = open(file_path)


	# skip over header (the first line)
	next(lunone)
	nl = 0
	for line in lunone:

		# get rid \n & blank line
		line = line.rstrip()	
		if not line: continue

		# split values into a list
		fields = line.split()
		h, p, s, whatever = tuple(fields)
		h = float(h)
		p = float(p)
		s = float(s)
		
		
		if nl > MAX1D:
			print(' Too many layers; maximum now is ', MAX1D)
			break


		if vs1d == 1:
			vp.append([p, s])
		else:
			vp.append([p, p/s])

		# ONE-TIME CLUDGE TO FORCE A VP/VS
		# vp(nl,2) = p/1.78
		z.append(h)
		terp.append(whatever[0])
		nl += 1

	# generate the model
	file_path = os.path.relpath("data/TW_m30_wL.mod")
	luncor = open(file_path, "wb")

	for n in [0, 1]:
		noff = nxyzc*n
		print('')
		print(' Lay   Dep      D1      D2      V1      V2      V      ZFL     VFL')
		lout.write('\n')
		lout.write(' Lay   Dep      D1      D2      V1      V2      V      ZFL     VFL\n')
		for k in range(0, nzc):
			koff = nxyc*k + noff
			zg = gz[k]
			for ik in range(1, nl):
				if z[ik] > zg: break

			ik = ik-1
			if terp[ik] == 'I':
				zk = z[ik]
				hz = z[ik+1] - zk
				fz = (zg-zk)/hz
				v = (1-fz)*vp[ik][n] + fz*vp[ik+1][n]
			else:
				v = vp[ik][n]

			#### flatten this wavespeed if necessary
			if iflat == 1:
				zfl = flatz(zg)
				vfl = flatvel(v,zfl)
			else:
				zfl = zg
				vfl = v

			print("%4d%8.2f%8.2f%8.2f%8.2f%8.2f%8.2f%8.2f%8.2f" % ((k+1), zg, z[ik], z[ik+1], vp[ik][n],vp[ik+1][n], v, zfl, vfl) )
			lout.write("%4d%8.2f%8.2f%8.2f%8.2f%8.2f%8.2f%8.2f%8.2f\n" % ((k+1), zg, z[ik], z[ik+1], vp[ik][n],vp[ik+1][n], v, zfl, vfl) )

			for j in range(0, nyc):
				joff = koff + nxc*j
				
				for i in range(0, nxc):
					vsave[joff+i] = vfl
			
	
	header_info = head
	header_info += ttype
	header_info += syst
	header_info += quant
	header_info += flatten
	header_info += hcomm
	

	for i in range(len(header_info), 120):
		header_info += ' '

	
	luncor.write(bytes(header_info, "ascii"))
	luncor.write(bytes(igridx))
	luncor.write(bytes(igridy))
	luncor.write(bytes(igridz))
	luncor.write(bytes(vsave[:nxyzc2]))


def flatvel(v, z):
	'''
	does earth-flattening correction for velocity, at depth z.
	assumes z is the flat-earth depth (already corrected). 12/87 gaa.
	a different transform is done for blocks, which have integrated
	average velocities
	'''

	r = 6371.00
	return exp(z / r) * v


def flatz(z):
	'''
	does earth-flattening correction from depth in spherical earth to
	depth in flat-earth.  this preserves travel-times if the velocity
	correction is also used.  see chapman (1973).  gaa 12/87.
	'''

	r = 6371.00
	return r * log(r / (r - z)) / log(exp(1))


def uflatz(z):
	'''
	undoes earth-flattening correction from depth in spherical earth to
	depth in flat-earth.  
	'''

	r = 6371.00
	return r*(1. - exp(-z/r))


def glat(hlat):
	#implicit real*8 (a-h, o-z)
	'''
	convert geographic latitude to geocentric latitude-------------
        hlat (input) = geographic latitude in radians (north positive)
        glat (output)= geocentric latitude in radians (north positive)
	-----------------------------------------------------------------
	'''

	halfpi, polfac, elfac = 1.570796, 0.010632, 0.993277
	if halfpi - fabs(hlat) >= float(0.05):
		return atan(elfac * sin(hlat) / cos(hlat))

	else:
		# special formula near pole
		return hlat / elfac - fabs(polfac) * (1 if hlat >= 0 else -1)
    
# 待修改 參數r
def glath(xlat, h, r):
	
	#implicit real*8 (a-h,o-z)
	'''
	ap is semi major axis, bp is semiminor axis, f is inverse flattening, esq is the square of
	the ellipticity, which we compute from fi*(2.d0-fi) where fi is 1/f.
	'''
	ap, bp, f = 6378137.0, 6356752.314245, 298.257223563
	esq = 6.69437978616733379 * 0.001    #-03
	degrad = 1.74532930056254081 * 0.01	 #D-02

	sinxl = sin(xlat)

	# convert depth in km to elevation in meters
	hm = -h * 1000.0

	# anu is the ellipsoidal radius of curvature at the current geographic latitude

	anu = ap / sqrt(1.0 - esq * sinxl * sinxl)

	x = (anu + hm) * cos(xlat)
	z = ((1.0 - esq) * anu + hm) * sinxl

	r = sqrt(x * x + z * z) / 1000.0
	return atan2(z, x)


def glathinv(xcent, r, h):

	#implicit real*8 (a-h,o-z)
	'''
	ap is semi major axis, bp is semiminor axis, f is inverse flattening, esq is the square of
	the ellipticity, which we compute from fi*(2.d0-fi) where fi is 1/f.
	'''
	ap, bp, f = 6378137.0, 6356752.314245, 298.257223563
	esq = 6.69437978616733379 * 0.001    #-03
	degrad = 1.74532930056254081 * 0.01	 #D-02

	# After about 5 iterations, the precision should be on the order of cm. We should
	# probably set a tolerance for this in any event

	maxitt = 5

	# convert to meters
	rm = r * 1000.0

	xlatr = xcent
	x = rm * cos(xlatr)
	z = rm * sin(xlatr)

	nitt = 1
	while nitt <= maxitt:
		sinxl = sin(xlatr)
		anu = ap / sqrt(1.0 - esq * sinxl * sinxl)
		hb = x / cos(xlatr) - anu
		zp = z / (1.0 - esq * (anu / (anu + hb)))
		xlatr = atan2(zp, x)
		nitt = nitt + 1
		# write(*,*) xlatr/degrad, hb
	    

	h = x / cos(xlatr) - anu
	h = -h / 1000.0
	return xlatr


#if __name__ == '__main__':
#    main()