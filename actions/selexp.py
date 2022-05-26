
'''
MESS action - [selexp]
locally exports the current status file selection to be reused later
'''

#-------------#-------------#-------------#-------------#-------------#-------------#
#IMPORTS

import actions.helper as helper
from os.path import join, splitext, exists, isdir, isfile
from datetime import date
import json

#-------------#-------------#-------------#-------------#-------------#-------------#
#VARIABLES

about = 'locally exports the current status file selection to be reused later.'
params = dict()

#-------------#-------------#-------------#-------------#-------------#-------------#
#FUNCTIONS

def prepare_params(status):
	
	print('export selection under which name? (16 chars max, letters only)')
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

	out = dict()
	out['fname']=line
	return out

def execute(params, status, v=False):
	fname = './selections/'+params['fname']+'.sel'
	fh = open(fname, 'w')
	fh.write(json.dumps(status.selection))
	fh.close()
	helper.v(v, 'successfully exported selection of '+str(len(status.selection))+' items to '+fname+'.')
	return status
