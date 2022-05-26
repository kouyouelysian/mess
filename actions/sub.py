
'''
MESS action - [sub]
sets status path to a subfolder of current path
if the subfolder doesn't exist, tries to create it
'''

#-------------#-------------#-------------#-------------#-------------#-------------#
# imports

import actions.helper as helper
from os.path import exists
from os.path import join
from os import makedirs

#-------------#-------------#-------------#-------------#-------------#-------------#
# functions

'''
ACTION METADATA - READ BY THE REST OF THE PROGRAM
'''

about = "goes to a subfolder in the status current working path. creates the folder if it's not there"
params = dict()

'''
PARAMETER PREPARE FUNCTION - CREATES AND CHECKS PARAMETERS NECESSARY FOR THIS ACTION
'''

def prepare_params(status):
	out = dict()
	print("Subfolder name? (will get created in working directory if not there)")
	sub = input("#: ")

	out['name']=sub

	return out


'''
ACTUAL ACTION RUNTIME - GETS PARAMETERS PREPARED IN prepare_params AND SEQUENCER STATUS
'''

def execute(params, status, v=False):
	if not exists(join(status.path, params['name'])):
		helper.v(v, 'subdir was not existing, created new...')
		makedirs(join(status.path, params['name']))
	status.path = join(status.path, params['name'])
	helper.v(v, 'new status path: ' + status.path)
	return status
