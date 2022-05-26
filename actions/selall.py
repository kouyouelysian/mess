
'''
MESS action - [selall]
selects all the files in status working path
'''

#-------------#-------------#-------------#-------------#-------------#-------------#import actions.helper as helper

from os.path import exists
from os.path import join
from datetime import date
import actions.helper as helper

'''
ACTION METADATA - READ BY THE REST OF THE PROGRAM
'''

about = 'selects all the files in status working path'
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
	all_fnames = helper.files_in_folder(status.path)
	all_files = []
	for fname in all_fnames:
		all_files.append(join(status.path, fname))
	status.selection = all_files
	return status
