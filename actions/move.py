
'''
MESS action - move
grabs file in current status selection and moves them to a specified place
'''

#-------------#-------------#-------------#-------------#-------------#-------------#
#imports

import actions.helper as helper
from os.path import exists
from os.path import join, basename
from os import replace as file_move

#-------------#-------------#-------------#-------------#-------------#-------------#

'''
ACTION METADATA - READ BY THE REST OF THE PROGRAM
'''

about = 'moves current selection of files to a selected folder. selection\
 is set to new locations of the same files'
params = dict()





'''
PARAMETER PREPARE FUNCTION - CREATES AND CHECKS PARAMETERS NECESSARY FOR THIS ACTION
'''

def prepare_params(status):
	
	absolute = False
	path = ""

	
	while (1):
		print("New path?")
		path = helper.get_path()
		if exists(path):
			break
		else:
			print('Path does not exist, please check and try again.')
			
	out = dict()
	out['path']=path
	return out


'''
ACTUAL ACTION RUNTIME - GETS PARAMETERS PREPARED IN prepare_params AND SEQUENCER STATUS
'''

def execute(params, status, v=False):

	dest = params['path']

	if not exists(dest):
		print('Destination folder not found - operation cancelled!')
		return

	for i in range(len(status.selection)):
		name = basename(status.selection[i])
		helper.v(v, 'moving '+status.selection[i]+' --> '+join(dest, name))
		file_move(status.selection[i], join(dest, name))
		status.selection[i] = join(dest, name)

	return status


	
