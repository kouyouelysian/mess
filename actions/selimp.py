
'''
MESS action - [selimp]
imports the locally saved status file selection to the current status
'''

#-------------#-------------#-------------#-------------#-------------#-------------#
#IMPORTS

import actions.helper as helper
from os.path import join, splitext, exists, isdir, isfile, splitext
from datetime import date
import json

#-------------#-------------#-------------#-------------#-------------#-------------#
#VARIABLES

about = 'imports the locally saved status file selection to the current status'
params = dict()

#-------------#-------------#-------------#-------------#-------------#-------------#
#FUNCTIONS

def prepare_params(status):

	out = dict()
	
	print("the existence check is NOT DONE here because a requested selection may be",
		"made during the sequence, and did not necessarily exist when the sequence was being",
		"programmerd. This action will return an empty selection and FAIL if file is not found.",
		"There currently are these selections:")

	for f in helper.files_in_folder("./selections/"):
		print(helper.filepath_getname(f))

	print('import selection of which name? (16 chars max, letters only)')
	line = ""
	while (1):
		line = input(":# ").strip().replace(" ", '_')
		if len(line)>16:
			print('name exceeds 16 characters, try again: ', line)
			continue
		if not helper.string_only_lettersnumbers(line):
			print('name contains something other than letters and numbers, try again: ', line)
			continue
		break

	print('should the action (F) fail or return an (E) empty selection if the sel file is not found?')
	opt = helper.get_opt(['F', 'E'])
	if (opt=='E'):
		out['onnofile']='returnempty'
	elif (opt=='F'):
		out['onnofile']='fail'

	
	out['fname']=line
	return out


def execute(params, status, v=False):


	fname = './selections/'+params['fname']+'.sel'
	try:
		fh = open(fname, 'r')
	except Exception as e:
		if (params['onnofile']=='returnempty'):
			helper.v(v, 'failed to import selection from: '+fname+" (returning empty selection)")
			status.selection = []
			return status
		elif (params['onnofile'=='fail']):
			raise FileNotFoundError('cannot read selection: '+fname)


	l = json.loads(fh.read())
	fh.close()

	status.selection = l
	helper.v(v, 'successfully imported selection of '+str(len(status.selection))+' items from '+fname+'.')

	return status
