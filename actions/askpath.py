
'''
MESS action - [askpath]
asks an absolute path mid-script, sets status path to it
'''

#-------------#-------------#-------------#-------------#-------------#-------------#
# imports

import actions.helper as helper
from os.path import exists
from os.path import join

#-------------#-------------#-------------#-------------#-------------#-------------#

'''
ACTION METADATA - READ BY THE REST OF THE PROGRAM
'''

about = 'displays a message and asks an absolute path mid-script, sets status path to it.'
params = dict()

'''
PARAMETER PREPARE FUNCTION - CREATES AND CHECKS PARAMETERS NECESSARY FOR THIS ACTION
'''

def prepare_params(status):
	
	out = dict()
	print("message to user?")
	message= input("#: ")	
	out['message']=message
	return out


'''
ACTUAL ACTION RUNTIME - GETS PARAMETERS PREPARED IN prepare_params AND SEQUENCER STATUS
'''

def execute(params, status, v=False):

	print(params['message'])

	while (1):
		print("(input an absolute path)")
		path = helper.get_path()
		if exists(path):
			break
		else:
			print('Path does not exist, please check and try again:', path)

	status.path = path 
	helper.v(v, 'new status path: ' + status.path)
	return status
