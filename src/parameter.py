#-------------------------------------------------------------------
#   These parameters set the general array dimensions among
#   common arrays by the various tomofd programs.
#
#	Fine grid specs:
#	
#	nxm 	Maximum number of grid points in 
#	nym		the x,y,z directions
#	nzm
#
#	Coarse grid specs:
#	
#	nxcm 	Maximum number of coarse grid points in 
#	nycm	the x,y,z directions
#	nzcm
#
#	Note that the programs calculate the number of find grid points
#	based on the coarse grid specs and node locations.
#
#	Bookkeeping:
#
#       maxsta	This is the total number of travel time tables that
#		routines like telrayderv can store while doing ray
#		calculations.  It will be more efficient to make this
#		number as large as your machines memory will allow, but
#		need not be any larger than the total number of tables
#		you have ( = number of stations in the station list or
#		twice that if you are using both P and S waves)
#	
#		maxobs	The maximum number of observations allowed per event
#
#		maxlst	The maximum number of stations in the station list
#
#   	maxnbk  The maximum number of variables accumulated by a single ray
#
#		maxkbl  The maximun number of variables accumulated by a single event
#
#		maxmbl  The maximun number of variables accumulated by the entire
#				dataset
#
#----Large matrices of normal equations
#
#       NMAX 	Maximum number of columns of A (total number of variables)
#
#       MMAX	Maximum number of rows of A (observations + constraints)
#
#       SIZEOFA Maximum number of elements of A
#
#--------------------------------------------------------------------

NMAX=None
MMAX=None
SIZEOFA=None
#----fine grid specs
# ****** crustal scale (1km
nxm=301
nym=301
nzm=61
nxym=nxm*nym
nxyzm=nxym*nzm
nxyzm2=nxyzm*2

#---coarse grid specs
nxcm=203
nycm=203
nzcm=105
nxycm=nxcm*nycm
nxyzcm=nxycm*nzcm
nxyzcm2=nxyzcm*2
nxcm1=nxcm-1
nycm1=nycm-1
nzcm1=nzcm-1
nblkcm=nxcm1*nycm1*nzcm1

#----bookkeeping
maxsta=2000
maxobs=800
maxlst=4000
maxlst2=2*maxlst
maxnbk=200000
maxkbl=100000
maxmbl=3000000

#----large matrices of normal equations
NMAX=2500000
MMAX=50000000
SIZEOFA=200000000
#----openmp
ncpu=20
maxtrd=1024