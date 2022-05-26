
'''
MESS action - movesub
grabs file in current status selection and moves them to a new subfolder in working folder
'''

#-------------#-------------#-------------#-------------#-------------#-------------#
#imports

import actions.helper as helper
from os.path import exists
from os.path import join, basename
from os import replace as file_move
from os import makedirs
from shutil import move

#-------------#-------------#-------------#-------------#-------------#-------------#

'''
ACTION METADATA - READ BY THE REST OF THE PROGRAM
'''

about = 'goes to/creates a subfolder of a name in working folder and moves the selection of files to it. selection is set to new locations of the same files'
params = dict()





'''
PARAMETER PREPARE FUNCTION - CREATES AND CHECKS PARAMETERS NECESSARY FOR THIS ACTION
'''

def prepare_params(status):
	

	subname = ""
	while (1):
		print("subfolder name? (letters and numbers only)")
		subname = input("#: ")
		if helper.string_only_lettersnumbers(subname):
			break
		else:
			print('please, only use letters and numbers')
			
	out = dict()
	out['subname']=subname
	return out


'''
ACTUAL ACTION RUNTIME - GETS PARAMETERS PREPARED IN prepare_params AND SEQUENCER STATUS
'''

def execute(params, status, v=False):

	newpath = join(status.path, params['subname'])
	makedirs(newpath, exist_ok=True) # creates a new subfolder. is ok if it is already there

	if not exists(newpath):
		print('Destination folder not found - operation cancelled!')
		return

	for i in range(len(status.selection)):
		name = basename(status.selection[i])
		helper.v(v, 'moving '+status.selection[i]+' --> '+join(newpath, name))
		move(status.selection[i], newpath)
		status.selection[i] = join(newpath, name)

	return status

	
