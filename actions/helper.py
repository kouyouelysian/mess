
'''
library of helper funcitons, to be shared by the actions
'''

#-------------#-------------#-------------#-------------#-------------#-------------#

from os.path import join, exists, isfile, isdir, splitext, basename
from os import listdir
from sys import platform

#-------------#-------------#-------------#-------------#-------------#-------------#

'''
tries to parse a string into an argument
False on fail, integer otherwise
'''
def parse_int(arg):
	out = 0
	try:
		out = int(arg)
	except Exception as e:
		return False
	return out

'''
safe input - integer. denies non-parsable inputs, asks until happy
'''
def get_int():
	out = 0;
	while(1):
		line = input("#: ")
		out = parse_int(line.strip())
		if (out == False):
			print('cannot parse as integer, try again: ', out)
		else:
			break
	return out


'''
safe input - integer with set ranges, denies inputs outisde of the range. asks until happy
'''
def get_int_range(lower=0, upper=100):
	out = 0;
	while (1):
		out = get_int()
		if (out < lower or out > upper):
			print('the value has to be in the following bounds (including):', lower, 'to', upper)
			continue
		else:
			break
	return out

'''
formatted input - prepares the path for further use
'''
def get_path():
	path = input("#: ")
	if (platform == 'darwin'):
		path = path.replace('\\', '') # delete space auto-backslashes
	return path.strip()

'''
safe input - option. one letter, for use in action menus.
takes in a list of allowed options, asks until user inputs one of them.
'''
def get_opt(allowed):
	allowed_str = ''
	for x in allowed:
		allowed_str += x.upper()+","
	allowed_str = allowed_str[:-1]
	arg = ""
	while (1):
		arg = input('#: ')
		arg = arg[:1].upper()
		if (arg in allowed):
			break
		else:
			print('Option not one of the allowed ('+allowed_str+'): ', arg)
	return arg


'''
safe input - extended option. one or more letters, for use in action menus.
takes in a list of allowed options, asks until user inputs one of them.
'''
def get_opt_ext(allowed):
	allowed_str = ''
	for x in allowed:
		allowed_str += x.upper()+","
	allowed_str = allowed_str[:-1]
	arg = ""
	while (1):
		arg = input('#: ')
		arg = arg.upper()
		if (arg in allowed):
			break
		else:
			print('Extended option not one of the allowed ('+allowed_str+'): ', arg)
	return arg


'''
returns the list of files in folder
'''
def files_in_folder(folder):
	if exists(folder):
		out = []
		li = listdir(folder)

		for e in li:
			if isfile(join(folder,e)):
				out.append(e)
		return out
	return False

'''
returns the list of folders in folder
'''
def folders_in_folder(folder):
	if exists(folder):
		out = []
		li = listdir(folder)

		for e in li:
			if isdir(join(folder,e)):
				out.append(e)
		return out
	return False

'''
gets just the filename form the path, e.g. /test/work/butt.png -> butt
'''
def filepath_getname(arg):
	return splitext(basename(arg))[0]


'''
see if the string is letters and numbers only
'''
def string_only_lettersnumbers(arg):
	letters = 'abcdefghijklmnopqrstuvwxyz1234567890'
	for l in arg:
		if (l not in letters):
			print(l)
			return False
	return True


'''
give it '180MB' - returns ['180', 'MB']
likewise '12345pingas' becomes ['12345', 'pingas']
so check what you feed it. used by sel, etc
'''
def split_volume_string(arg):
	numbers = '0123456789'
	unit = arg
	for n in numbers:
		unit = unit.replace(n, '')
	value = arg.replace(unit, '')
	return [value, unit]

'''
debug print if verbose is on
'''

def v(verbose, contents):
	if verbose:
		print(contents)