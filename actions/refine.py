
'''
MESS action - [refine]
refines the status selection by a certain condition
'''

#-------------#-------------#-------------#-------------#-------------#-------------#import actions.helper as helper

from os.path import exists
from os.path import join, splitext, getsize, getctime, getmtime
from datetime import date
import actions.helper as helper

'''
ACTION METADATA - READ BY THE REST OF THE PROGRAM
'''

about = 'refines the status selection by a certain condition.'
params = dict()





'''
PARAMETER PREPARE FUNCTION - CREATES AND CHECKS PARAMETERS NECESSARY FOR THIS ACTION
'''

def prepare_params(status):
	
	print("Select the condition:\n(N) fileName contians\n(E) file Extension is\n"+
		"(M) filesize is More or equal then\n(L) filesize is Less or equal then\n"+
		"(CE) creation date earlier than\n(CL) creation date later than\n"+
		"(ME) modification date earlier than\n(ML) modification date later than\n")


	letters = ['N','E','M','L', 'CE', 'CL', 'ME','ML']
	
	conditions = ["name", "extension", "size_more", "size_less", "cdate_earlier", "cdate_later", "mdate_earlier", "mdate_later"]
	condition = ""
	opt = helper.get_opt_ext(letters)
	for x in range(len(letters)):
		if (opt == letters[x]):
			condition = conditions[x]

	value = None

	if (opt == 'N'):
		print('Enter a string that will be looked for as part of the filename/the whole filename to select:')
		line = input("#: ")
		value = str(line.strip())
	elif (opt == 'E'):
		print('Enter the file extension of the files you wish to select:')
		line = input("#: ")
		value = str(line.strip())
	elif (opt == 'M' or opt == 'L'):
	
		while (1):
			print('Enter the threshold filesize (number + unit, e.g. 180MB):')
			line = input("#: ")
			line = line.upper().strip()

			parts = helper.split_volume_string(line)
			if (len(parts)!=2) or (parts[1] not in ['B','KB','MB','GB','TB']):
				print('cannot parse the filesize string: ', parts)
				continue
			value = line
			break
	elif (opt in ['ME', 'ML', 'CE','CL']):
		print("Enter the year of the threshold date:")
		year = helper.get_int_range(1900, 3000)
		print("Enter the month (01 - 12) of the threshold date:")
		month = helper.get_int_range(1, 12)
		print("Enter the day of the threshold date")
		days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
		if (month == 2 and year%4==0):
			days[1] = 29 # the cool thing february does once in a while

		day = helper.get_int_range(1, days[month-1])
		value = date(year, month, day)



	out = dict()
	out['condition']=condition
	out['value']=value
	return out


'''
ACTUAL ACTION RUNTIME - GETS PARAMETERS PREPARED IN prepare_params AND SEQUENCER STATUS
'''
def execute(params, status, v=False):
	
	files = []
	all_files = status.selection
	if (all_files == False):
		print('No directory at:',status.path)
		return status
	helper.v(v,'all files:')
	for f in all_files:
		helper.v(v, "- "+f)
	helper.v(v,'\nselected:')

	# select by name/extension
	if (params['condition'] == 'name' or params['condition'] == 'extension'): # by name
		for f in all_files:
			parts = splitext(f)
			if (params['value'] in parts[0] and params['condition'] == 'name') or\
			(params['value'] in parts[1] and params['condition'] == 'extension') :
				helper.v(v, '+++ '+f)
				files.append(join(status.path, f))
	
	# select by size
	elif (params['condition']=='size_less' or params['condition']=='size_more'):
		d = {'B':0,'KB':1,'MB':2,'GB':3,'TB':4}
		line = params['value']
		value, unit = helper.split_volume_string(line)
		helper.v(v, "target value "+value+",unit "+unit)
		power = d[unit]
		mul = 1	
		for x in range(power):
			mul*= 1024
		targetsize=mul*int(value)
		helper.v(v, 'requested threshold, bytes: '+str(targetsize))
		for f in all_files:
			size = getsize(join(status.path, f))	
			if (params['condition']=='size_more') and (size>targetsize):
				helper.v(v, '+++ '+f+" ("+str(size)+">"+str(targetsize)+")")
				files.append(join(status.path, f))
			if (params['condition']=='size_less') and (size<targetsize):
				helper.v(v, '+++ '+f+" ("+str(size)+"<"+str(targetsize)+")" )
				files.append(join(status.path, f))	

	# select by creation date
	elif (params['condition']=='cdate_earlier' or params['condition']=='cdate_later'):
		targetdate = params['value']
		helper.v(v, "target date "+str(targetdate))
		for f in all_files:
			filedate = getctime(join(status.path, f))
			filedate = date.fromtimestamp(filedate)
			if (params['condition']=='cdate_earlier' and filedate<=targetdate):
				helper.v(v, '+++ '+f+' | '+str(filedate))
				files.append(join(status.path, f))
			if (params['condition']=='cdate_later' and filedate>=targetdate):
				helper.v(v, '+++ '+f+' | '+str(filedate))
				files.append(join(status.path, f))


	# select by modification date
	elif (params['condition']=='mdate_earlier' or params['condition']=='mdate_later'):
		targetdate = params['value']
		helper.v(v, "target date "+str(targetdate))
		for f in all_files:
			filedate = getmtime(join(status.path, f))
			filedate = date.fromtimestamp(filedate)
			if (params['condition']=='mdate_earlier' and filedate<=targetdate):
				helper.v(v, '+++ '+f+' | '+str(filedate))
				files.append(join(status.path, f))
			if (params['condition']=='mdate_later' and filedate>=targetdate):
				helper.v(v, '+++ '+f+' | '+str(filedate))
				files.append(join(status.path, f))


	status.selection = files
	return status
