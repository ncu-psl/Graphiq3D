from parameter import *
import struct
import numpy as np

# return (m, nbl, jndx, a, na, ja, b)
def  makea(m, nbl, lundts, lunres, lout,
 		jndx, a, na, ja, b):
	
	l = 0
	mm = 0
	lundts = open("data/dtds.out", "rb")

	while(True):

		namm = get_namm(lundts, lout)
		if namm == -1:
			break

		junk = lundts.read(4)
		header, = struct.unpack('i', lundts.read(4))
		

		b[mm] = get_b(lunres, mm, lout)
			

		l1 = l
		l2 = l + namm + 1
		l3 = l2
		if l3 > SIZEOFA:
			print(" FATAL ERROR (makea):  work array a is full")
			print(" Increase size parameter SIZEOFA in source code")
			lout.write(" FATAL ERROR (makea):  work array a is full\n")
			lout.write(" Increase size parameter SIZEOFA in source code\n")

		for i in range(l1, l2-1):
			ja[i], = struct.unpack('i', lundts.read(4))
			a[i], = struct.unpack('f', lundts.read(4))
			ja[i] -= 1

		ender, = struct.unpack('i', lundts.read(4))
		

		for i in range(l1, l2-1): 
				if ja[i] > NMAX:
					print(" FATAL ERROR (makea):  grid overflow")
					print(" Datum number %d(row)" % mm)
					lout.write(" FATAL ERROR (makea):  grid overflow \n")
					lout.write(" Datum number %d(row)\n" % mm)
					
		na[mm] = namm
		l = l2 - 1
		mm += 1
		if mm > MMAX:
			print(" FATAL ERROR (makea):  grid overflow ")
			print(" Maximum allowed number of rows = %d(rows)" % MMAX);
			lout.write(" FATAL ERROR (makea):  grid overflow \n");
			lout.write(" Maximum allowed number of rows = %d(rows)\n" % MMAX);

	print(" %10d rows of vel, hyp, and data read in \n" % mm);
	lout.write(" %10d rows of vel, hyp, and data read in \n" % mm);


	junk, = struct.unpack('i', lundts.read(4))
	junk, = struct.unpack('i', lundts.read(4))
	nbl, = struct.unpack('i', lundts.read(4))
	size, = struct.unpack('i', lundts.read(4))
	junk, = struct.unpack('i', lundts.read(4))

	jndx = np.fromfile(lundts, dtype=np.int32, count=nbl)
	if jndx == []:
		print("error on read jndx: fp_dts")

	m = mm
	print(" A total of %12d  rows read in " % m)
	print(" A total of %12d  elements of A read in " % l)
	print(" Total number of variables = %14d " % nbl)
	lout.write(" A total of %12d  rows read in \n" % m)
	lout.write(" A total of %12d  elements of A read in \n" % l)
	lout.write(" Total number of variables = %14d \n" % nbl)		


	return (m, nbl, jndx, a, na, ja, b)


# return namm or None(EOF)
def get_namm(inputFile, errorFile):

	junk = inputFile.read(4)
	data = inputFile.read(4)
	

	if data == None:
		print(" Error: Ran out of velocity info!")
		lout.write(" Error: Ran out of velocity info!\n")
		return None

	else:
		junk, = struct.unpack('i',junk)
		namm, = struct.unpack('i',data)

		
		return namm
		 


# return bmm or None(EOF)
def get_b(inputFile, mm, errorFile):

	try:
		junk = inputFile.read(4)
		if junk == None: 
			raise EOFError

		if mm != 0:
			junk = inputFile.read(4)
			if junk == None: 
				raise EOFError

		data = inputFile.read(4)
		if data == None: 
			raise EOFError

	except EOFError as error:
		print(" Error: Ran out of data!")
		lout.write(" Error: Ran out of data!\n")
		return None


	bmm, = struct.unpack('f',data)
	
	return bmm






