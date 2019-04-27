#!/usr/bin/env python3
import os
from parameter import *
from gridspec import *
from parseprogs import *
from math import *
import numpy as np
import re
import sys,time

np.seterr(all='raise')

# returns v
def find_vel(x, y, z, iph,gx,gy,gz,vp,nxyzc,nxc,nyc,nzc):

    for i in range(1, nxc):
        if gx[i] > x:
            break	
	
    i-=1
    xi = gx[i]
    hx = gx[i + 1] - xi
    
    
    for j in range(1, nyc):
        if gy[j] > y:
            break
		
	
    j-=1
    yj = gy[j]
    hy = gy[j + 1] - yj

    for k in range(1, nzc):
        if gz[k] > z:
            break
	
	
    k-=1
    zk = gz[k]
    hz = gz[k + 1] - zk
	
    nk = nxc * nyc * k
    nj = nxc * j
    nk2 = nxc * nyc * (k + 1)
    nj2 = nxc * (j + 1)
    fx = (x - xi) / hx
    fy = (y - yj) / hy
    fz = (z - zk) / hz
    i = i + iph * nxyzc
	
    v = (1. - fx) * (1. - fy) * (1. - fz) * vp[nk + nj + i]
    v = v + fx * (1. - fy) * (1. - fz) * vp[nk + nj + i + 1]
    v = v + (1. - fx) * fy * (1. - fz) * vp[nk + nj2 + i]
    v = v + (1. - fx) * (1. - fy) * fz * vp[nk2 + nj + i]
    v = v + fx * fy * (1. - fz) * vp[nk + nj2 + i + 1]
    v = v + fx * (1. - fy) * fz * vp[nk2 + nj + i + 1]
    v = v + (1. - fx) * fy * fz * vp[nk2 + nj2 + i]
    v = v + fx * fy * fz * vp[nk2 + nj2 + i + 1]
    
    return v

def mainn():
    
	MAX1D=1000

	mustv = 4
	mustf = 2

	nhbyte = 58

	# common area
	gx = []
	gy = []
	gz = []

	vp = []

	head = ttype = syst = quant = flatten = \
	hcomm = fxs = fys = fzs = clat = clon = cz = \
	axo = ayo = azo = dx = dy = dz = az = nxh = nyh = nzh = None
	# --------

	vsave = np.zeros(nxyzm2, dtype=np.float32)

	mvals = ["nxc", "nyc", "nzc", "h"]
	files = ["oldvfil", "tgrdfil", "finevel"]
	rearth, degrad, hpi = 6371.0, 0.017453292, 1.570796
	VERSION = "2004.0909"

	lenhead = nhbyte*4

	# Default setting for some variables
	x0 = 0.
	y0 = 0.
	z0 = 0.

	ittnum = 1

	# End of default values


		
	# this line is for testing only, replace with the line below this one
	specfile = os.path.relpath("FDtomo.spec")
	#specfile = input(' Enter parameter specification file: ')
	lunspc = open(specfile)

	#### Recover the variables (must) needed to run this program
	#
	#       nxc, nyc, ggnzc      coarse dimensions of the fine mesh used in the trt tables
	#       h                  fine grid spacing
	#
	#global nxc, nyc, nzc, nxyzc 

	nxc = int(getvars(lunspc, mvals[0], 1))
	nyc = int(getvars(lunspc, mvals[1], 1))
	nzc = int(getvars(lunspc, mvals[2], 1))
	h = float(getvars(lunspc, mvals[3], 1))
	oldvfil = getvars(lunspc, files[0], 1)
	tgrdfil = getvars(lunspc, files[1], 1)
	finevel = getvars(lunspc, files[2], 1)

	#### Optionally read in some variables

	# Coordinate origin (used in header)
	x0 = float(getvars(lunspc, "x0"))
	y0 = float(getvars(lunspc, "y0"))
	z0 = float(getvars(lunspc, "z0"))
	clat = float(getvars(lunspc, "clat"))
	clon = float(getvars(lunspc, "clon"))
	cz = getvars(lunspc, "cz")
	azmod = getvars(lunspc, "azmod")
	ittum = int(getvars(lunspc, "ittum"))

	# Grid specs
	igridx = [int(x) for x in getvars(lunspc, "igridx")]
	igridy = [int(x) for x in getvars(lunspc, "igridy")]
	igridz = [int(x) for x in getvars(lunspc, "igridz")]

	#### End of optional parameters

	nxyc = nxc*nyc
	nxyzc = nxyc*nzc
	nxyzc2 = nxyzc*2

	nx = 1
	ny = 1
	nz = 1

	gx.append(x0)
	gy.append(y0)
	gz.append(z0)

	for i in range(1, nxc):
		nx = nx + igridx[i-1]
		gx.append(gx[i-1] + h*igridx[i-1])
	for i in range(1, nyc):
		ny = ny + igridy[i-1]
		gy.append(gy[i-1] + h*igridy[i-1])
	for i in range(1, nzc):
		nz = nz + igridz[i-1]
		gz.append(gz[i-1] + h*igridz[i-1])

	nxy = nx*ny
	nxyz = nxy*nz
	nxyz2 = nxyz*2

	logfile = "data/c2f.log" + str(ittnum)
	lout = open(logfile, 'w')

	lout.write(" \n")
	lout.write(" *************************************************************** \n")
	lout.write("          Parameters Set For This Run of c2f.f\n")
	lout.write("\n")
	lout.write(" c2f VERSIO: %s\n" % VERSION)
	lout.write("\n")
	lout.write(" Current parameter specification file: %-40s\n" % specfile)
	lout.write("\n")
	lout.write(" Iteration counter: %19d\n" % ittnum)
	lout.write("\n")
	lout.write(' Cartesian X origin (x0):    %.16lf\n' % x0)
	lout.write(' Cartesian Y origin (y0):    %.16lf\n' % y0)
	lout.write(' Cartesian Z origin (z0):    %.16lf\n' % z0)
	lout.write(' Fine grid spacing: %.16lf\n' % h)
	lout.write('\n')
	lout.write(' Number of X coarse grid nodes: %d\n' % nxc)
	lout.write(' X coarse grid node spacing: \n')
	for i in range(0, nxc-1):
			lout.write(str(igridx[i])+'   ')
			if i%10 == 9:
				lout.write('\n')

	lout.write('\n\n')
	lout.write(' Number of Y coarse grid nodes: %d\n' % nyc)
	lout.write(' Y coarse grid node spacing: \n')
	for i in range(0, nyc-1):
			lout.write(str(igridy[i])+'   ')
			if i%10 == 9:
				lout.write('\n')

	lout.write('\n\n')
	lout.write(' Number of Z coarse grid nodes: %d\n' % nzc)
	lout.write(' Z coarse grid node spacing: \n')
	for i in range(0, nzc-1):
			lout.write(str(igridz[i])+'   ')
			if i%10 == 9:
				lout.write('\n')

	lout.write('\n\n')
	lout.write(' Number of X fine grid nodes: %d\n' % nx)
	lout.write(' Number of Y fine grid nodes: %d\n' % ny)
	lout.write(' Number of Z fine grid nodes: %d\n' % nz)
	lout.write('\n')
	lout.write(' Total Number of fine grid nodes: %d\n' % nxyz)
	lout.write(' Total Number of coarse grid nodes: %d\n' % nxyzc)
	lout.write('\n')
	lout.write(' Input file attachments:\n')
	lout.write('\n')
	lout.write(' Current Wavespeed model file: %-40s\n' % oldvfil)
	lout.write('\n')
	lout.write(' Output file attachments:\n')
	lout.write('\n')
	lout.write(' Grid output file:             %-40s\n' % tgrdfil)
	lout.write(' P&S fine model:               %-40s\n' % finevel)
	lout.write(' P only fine model (*.pvel):   %-40s\n' % finevel)
	lout.write(' S only fine model (*.svel):   %-40s\n' % finevel)

	lout.close()

	# temporary output of grid for testing.  This will not be coorect
	# for spherical coordinates.
	tgrdfil = os.path.relpath("data/"+tgrdfil)
	luntgd = open(tgrdfil, 'w')

	for i in range(0, nxc):
		luntgd.write('%f    %f\n' % (gx[i], gy[0]) )
		luntgd.write('%f    %f\n' % (gx[i], gy[nyc-1]) )
	for i in range(0, nyc):
		luntgd.write('%f    %f\n' % (gx[0], gy[i]) )
		luntgd.write('%f    %f\n' % (gx[nxc-1], gy[i]))

	luntgd.close()

	cfile = oldvfil
	ffile = finevel

	cfile_path = os.path.relpath( cfile)
	luncor = open(cfile_path, "rb")

	# binary_data = luncor.read(4)
	# head = binary_data.decode('utf-8')
	# binary_data = luncor.read(4)
	# ttype = binary_data.decode('utf-8')
	# binary_data = luncor.read(4)
	# syst = binary_data.decode('utf-8')
	# binary_data = luncor.read(4)
	# quant = binary_data.decode('utf-8')
	# binary_data = luncor.read(4)
	# flatten = binary_data.decode('utf-8')

	binary_data = luncor.read(nhbyte)
	hdr = binary_data.decode('utf-8')
	head = hdr[:4]
	ttype = hdr[4:8]
	syst = hdr[8:12]
	quant = hdr[12:16]
	flatten = hdr[16:20]
	hcomm = hdr[20:]

	luncor.close()

	if head != 'HEAD':
		print(' File does not contain valid header...attempting headerless read ')
		lenrec = 4*nxyzc2
		luncor = open(cfile_path, "rb")
		vp = np.fromfile(luncor, dtype=np.float32, count=nxyzc2)
	

 		# set trial header values
		head = "HEAD"
		syst = "CART"
		quant = "BMOD"
		flatten = "NOFL"
		clath = clat
		clonh = clon
		czh = cz
		azh = azmod
		axo = x0
		ayo = y0
		azo = z0
		dxh = h
		dyh = h
		dzh = h
		nxh = nxc
		nyh = nyc
		nzh = nzc

		luncor.close()

	else:
		if ttype != "CORS":
			print(' WARNING: input mesh does not appear to be COARSE: ', ttype)
		if quant != "BMOD":
			print(' WARNING: file does not appear to be a valid type: ', quant)

		print(' Reading in Coarse Mesh ... ')
		lengrd = 4*(nxc + nyc + nzc - 3)
		lenrec = lenhead + lengrd + 4*nxyzc2
		luncor = open(cfile_path, "rb")


		# ignore first few bytes cause hdr[] was read and set before already
		luncor.seek(120)

		igridx = np.fromfile(luncor, dtype=np.int32, count=nxc-1)
		igridy = np.fromfile(luncor, dtype=np.int32, count=nyc-1)
		igridz = np.fromfile(luncor, dtype=np.int32, count=nzc-1)
		vp = np.fromfile(luncor, dtype=np.float32, count=nxyzc2)


		luncor.close()

	print('.. Done')
    
    
	# convert to slowness
	for i in range(0, nxyzc2):
		vp[i] = 1/vp[i]

	print('Interpolating ... ')
	# interpolation
	task_progress = 2*nz*ny*nx
	current_progress = 0
	ij = 0
	for n in [0, 1]:
		iph = n
		joff = ny * nz * n
		for k in range(0, nz):
			z = z0 + k * h
			nk2 = k * ny + joff
			for j in range(0, ny):
				y = y0 + j * h
				for i in range(0, nx):
					x = x0 + i * h
					v = find_vel(x, y, z, iph,gx,gy,gz,vp,nxyzc,nxc,nyc,nzc)
					# convert back to velocity
					vsave[ij] = 1/ v
					ij+=1



	print(".. Done")
	#graphic.draw(vsave)
	# redefine mesh type to be "FINE"
	type = "FINE"


	hcomm = "Output from c2f.f Version %s using %s" % (VERSION, oldvfil)

	nxh = nx
	nyh = ny
	nzh = nz

	# write out
	lengthp = ffile.find(' ')
	if lengthp == -1:
		vpfile = ffile
		vsfile = ffile
	else:
		vpfile = ffile[:lengthp]
		vsfile = ffile[:lengthp]

	vpfile = vpfile + '.pvel'
	vsfile = vsfile + '.svel'

	ffile_path = os.path.relpath("data/" + ffile)
	lunfnw = open(ffile_path, "wb")
	vpfile_path = os.path.relpath("data/" + vpfile)
	lunfnp = open(vpfile_path, "wb")
	vsfile_path = os.path.relpath("data/" + vsfile)
	lunfns = open(vsfile_path, "wb")



	print(' Writing out file 1... ')
	quant = "BMOD"
	lunfnw.write(bytes(hdr, "ascii"))
	lunfnw.write(bytes(vsave))

	print(' Writing out file 2... ')
	quant = "VPMD"
	np.savetxt("data/tempvel.pvel", vsave, delimiter=",")

	# lunfnp.write(str(hdr))
	# lunfnp.write(str(vsave[:nxyz]))

	print(' Writing out file 3... ')
	quant = "VSMD"
	lunfns.write(bytes(hdr, "ascii"))
	lunfns.write(bytes(vsave[nxyz:]))

	lunfnw.close()
	lunfnp.close()
	lunfns.close()


#if __name__ == '__main__':
#    main()