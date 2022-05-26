
'''
MESS action - [path]
sets status path to an absolute path,
'''

#-------------#-------------#-------------#-------------#-------------#-------------#
# imports

import actions.helper as helper
from os.path import exists
from os.path import join

#-------------#-------------#-------------#-------------#-------------#-------------#
# functions

'''
ACTION METADATA - READ BY THE REST OF THE PROGRAM
'''

about = 'sets the status current working path used by following actions, until explicitly\
changed by another pathset or other status altering command.'
params = dict()

'''
PARAMETER PREPARE FUNCTION - CREATES AND CHECKS PARAMETERS NECESSARY FOR THIS ACTION
'''

def prepare_params(status):
	out = dict()
	while (1):
		print("New path?")
		path = helper.get_path()
		if exists(path):
			break
		else:
			print('Path does not exist, please check and try again:', path)	
	out['path']=path
	return out


'''
ACTUAL ACTION RUNTIME - GETS PARAMETERS PREPARED IN prepare_params AND SEQUENCER STATUS
'''

def execute(params, status, v=False):
	status.path = params['path']
	helper.v(v, 'new status path: ' + status.path)
	return status
