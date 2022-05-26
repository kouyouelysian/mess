
'''
MESS action - [attention]
displays a message to the user and asks to press enter to continue
use to display important information about the sequence, etc
'''

#-------------#-------------#-------------#-------------#-------------#-------------#
#IMPORTS

import actions.helper as helper
from os.path import join, splitext, exists, isdir, isfile
from datetime import date

#-------------#-------------#-------------#-------------#-------------#-------------#
#VARIABLES

about = 'displays a message to the user and asks to press enter to continue. use to display important information about the sequence, etc'
params = dict()

#-------------#-------------#-------------#-------------#-------------#-------------#
#FUNCTIONS

def prepare_params(status):
	out = dict()
	print('what message should be displayed?')
	msg = input('#: ')
	out['msg']=msg
	return out

def execute(params, status, v=False):
	print("\n")
	print(params['msg'])
	print("press enter to continue...")
	input()

	return status
