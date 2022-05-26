
'''
MESS action - [actionname]
actiondescription
'''

#-------------#-------------#-------------#-------------#-------------#-------------#
#IMPORTS

import actions.helper as helper
from os.path import join, splitext, exists, isdir, isfile
from datetime import date

#-------------#-------------#-------------#-------------#-------------#-------------#
#VARIABLES

'''
ACTION METADATA - READ BY THE REST OF THE PROGRAM
replace about with relevant info.
'''

about = 'template of a MESS action script.'
params = dict()

#-------------#-------------#-------------#-------------#-------------#-------------#
#FUNCTIONS

'''
PARAMETER PREPARE FUNCTION - CREATES AND CHECKS PARAMETERS NECESSARY FOR THIS ACTION
in this function, ask the user for parameters using the CLI, if necessary
printing is allowed. please start inputs on new line with a ':# ' as the input text
'''

def prepare_params(status):

	out = dict()
	
	'''
	useful stuff:
	
	status.selection - current selection of files
	status.path - current working path

	helper.get_int() - safe integer input, loops until good
	helper.get_int_range(minb, maxb) - same, but also checks range, limits included
	helper.get_opt(['A', 'B'...]) - safe one-letter option input, 
	                                checks with the dict of allowed opts. loops till good.
	helper.get_path(arg) - formatted path input. does NOT check if path exists.
	helper.files_in_folder(arg) - returns list of files (not folders) in a folder of path arg
	helper.folders_in_folder(arg) - same but for folders

	'''
	

	
	out['param1']=val1
	out['param2']=val2
	#... ... ...
	return out


'''
ACTUAL ACTION RUNTIME - GETS PARAMETERS PREPARED IN prepare_params AND SEQUENCER STATUS
this function may alter the files as implied by its functionality, AND alter the sequencer status
by changing its working path, file selection etc.
If status isn't modified, return status anyways!!!
'''
def execute(params, status, v=False):

	
	'''
	useful stuff:
	
	status.selection - current selection of files
	status.path - current working path
	
	helper.get_int() - safe integer input, loops until good
	helper.get_int_range(minb, maxb) - same, but also checks range, limits included
	helper.get_opt(['A', 'B'...]) - safe one-letter option input, 
	                                checks with the dict of allowed opts. loops till good.
	helper.get_path(arg) - formatted path input. does NOT check if path exists.
	helper.files_in_folder(arg) - returns list of files (not folders) in a folder of path arg
	helper.folders_in_folder(arg) - same but for folders

	'''

	return status
