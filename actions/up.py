
'''
MESS action - [up]
sets status path one folder layer up
'''

#-------------#-------------#-------------#-------------#-------------#-------------#
# imports

import actions.helper as helper
from os.path import exists
from os.path import join
from os.path import split as psplit

#-------------#-------------#-------------#-------------#-------------#-------------#
# functions

'''
ACTION METADATA - READ BY THE REST OF THE PROGRAM
'''

about = 'makes status working path go one folder layer up'
params = dict()

'''
PARAMETER PREPARE FUNCTION - CREATES AND CHECKS PARAMETERS NECESSARY FOR THIS ACTION
'''

def prepare_params(status):
	out = dict()
	return out


'''
ACTUAL ACTION RUNTIME - GETS PARAMETERS PREPARED IN prepare_params AND SEQUENCER STATUS
'''

def execute(params, status, v=False):
	status.path = psplit(status.path)[0]
	helper.v(v, 'new status path: ' + status.path)
	return status
