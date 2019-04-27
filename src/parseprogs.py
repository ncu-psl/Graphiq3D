import sys, os
from pprint import pprint

def getvars_org(vname):
	'''
	Retreive variables from file

	Args:
		vname: target variable name to retreive

	Returns:
		parval: may be a string or a list of strings, depends on which variable. (return None when failed)
	'''

	file_path = os.path.relpath("../Archive/runs_ls/taiwan.nspec_sph01")
	parval = []
	mode = 1 # 1 when normal, 0 when '\' encountered(continue mode)  

	with open(file_path) as file:
		
		for line in file:

			# get rid \n
			line = line.rstrip()

			# ignore empty or comment line
			if not line or line[0] == '#':
				continue
			
			# find target param or continue on getting values
			fields = line.split()
			if fields[0] == vname or mode == 0:

				# if mode = 1 aka. not continue mode  =>  don't need to read fields[0]
				for val in fields[mode:]:
					if val[0] == '#':
						break
					else:
						parval.append(val)

				mode = 1
				if parval[-1] == '\\':
					parval.pop()
					mode = 0
			else:
				continue
				

				 	
	if len(parval) == 1:
		return parval[0]
	elif len(parval) > 1:
		return parval
	else:
		return None




def getvars(file, vname, raiseError=0):
	'''
	Retreive variables from file (rewind the file pointer everytime called)

	Args:
		file: target file object 
		vname: target variable name to retreive

	Returns:
		parval: may be a string or a list of strings, depends on which variable.
				raise Exception when failed to find parameter
				return 0 when raiseError is not set
	'''

	
	parval = []
	mode = 1 # 1 when normal, 0 when '\' encountered(continue mode)  

	file.seek(0)		
	for line in file:

		# get rid \n
		line = line.rstrip()

		# ignore empty or comment line
		if not line or line[0] == '#':
			continue
		
		# find target param or continue on getting values
		fields = line.split()
		if fields[0] == vname or mode == 0:

			# if mode = 1 aka. not continue mode  =>  don't need to read fields[0]
			for val in fields[mode:]:
				if val[0] == '#':
					break
				else:
					parval.append(val)

			mode = 1

			if parval[-1] == '\\':
				parval.pop()
				mode = 0
			else:
				break

		else:
			continue
				

				 	
	if len(parval) == 1:
		return parval[0]
	elif len(parval) > 1:
		return parval
	else:
		if raiseError:
			raise Exception(" Error trying to read variable ", vname)
		else:
			return 0


def getfields(file):
	'''
	Retreive a line from file & return the splitted line (as a list) 
	Args:
		file: target file object 
		
	Returns:
		fields: a tuple of value from a single line (unknown length)

	'''			

	line = file.readline()

	if not line:
		return  None

	# get rid \n
	line = line.rstrip()
	
	# split values into a list
	fields = line.split()

	return tuple(fields)

if __name__ == "__main__":
	val = getvars_org("nyc")
	print(val)

