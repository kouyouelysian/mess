
'''
CLI
'''

#-------------#-------------#-------------#-------------#-------------#-------------#
#IMPORTS

from modules import common
from modules.common import sequence_action, sequence_status, v
from actions.helper import files_in_folder
from os.path import join, basename, exists, splitext

#-------------#-------------#-------------#-------------#-------------#-------------#
#FUNCTION DEFINITIONS

def prepare_sequence_action(seq_action_name):
	global status
	global V
	print('#-------------- preparing '+'['+seq_action_name+']')
	module = common.arm_action(seq_action_name)
	f = getattr(module, 'prepare_params')
	params = f(status)
	o = sequence_action(seq_action_name, params) # make object to put to sequence
	#print('#--- PREPARED: '+o.name+", "+str(o.params))
	return o


'''
runs action by commom.sequence_action instance
'''
def run_action(t, i='---'):
	global status
	global V
	module = common.arm_action(t.name)
	f = getattr(module, 'execute')
	print('#-------------- running '+common.format_seq_num_str(i)+'['+t.name+']')
	if (CATCHFAILS):
		try:
			status = f(t.params, status, V)
		except Exception as e:
			print('FAILED: ', t.name, t.params, e)
		else:
			print('#--- SUCCESS: '+t.name+", "+str(t.params))
	else:
		status = f(t.params, status, V)
		print('#--- SUCCESS: '+t.name+", "+str(t.params))
	return


def main():
	
	global available_actions
	global status
	global sequence
	global V

	print('\n\n-----------------------------------------------')
	print('                    MESS')
	print('(multifunctional extendable sequencer solution)')
	print('-----------------------------------------------\n\n')

	print("enter action, dial in sequence number and action, or run a menu command. type 'help' to get help.\n")
	
	#cli loop
	while (True):

		

		line = input("#: ").strip()


		# special commands

		if (line == ''):
			continue

		elif (line == 'run'):
			# start running the sequence
			for i in range(SEQ_MAX):
				if (i in sequence):
					t = sequence[i] # get a sequence_action instance
					run_action(t, i)
			print('')

		elif (line == 'exit'):
			break

		elif (line[:4] == 'help'):

			fname = 'help'
			if len(line.split(' '))==2:
				parts = line.split(' ')
				fname = parts[1].strip().lower()
			fh = None
			try:
				fh = open('./textfiles/'+fname+'.txt', 'r')
			except Exception as e:
				print('cannot locate further help file:', './textfiles/'+fname+'.txt')
				print("run 'help' to see available further help files\n")
				continue
			else:
				print(fh.read())
				fh.close()

			


			

		elif (line == 'about'):
			common.cls()
			fh = open('./textfiles/about.txt', 'r')
			print(fh.read())
			fh.close()


		elif (line == 'actions'):
			for a in available_actions:
				print (a)
			print('')

		elif (line == 'c'):
			common.cls()

		elif (line == 'list'):
			for i in range(SEQ_MAX):
				if (i in sequence):
					print(common.format_seq_num_str(i), sequence[i])
			print('')
		elif (line == 'catchfails'):
			if (V):
				CATCHFAILS = False
				print('Action fails will stop the program and display traceback.')
			else:
				CATCHFAILS = True
				print('Action fails will be caught and briefly explained, program will keep running.')
			print('')
		elif (line == 'verbose'):
			if (V):
				V = False
				print('Verbose display has been turned off.')
			else:
				V = True
				print('Verbose display has been turned on.')
			print('')

		elif (line == 'status'):
			print(status)

		elif (line == 's'):
			for f in status.selection:
				print(f)
			print('total files selected:', len(status.selection))
			print('')

		elif (line == 'p'):
			print(status.path)
			print('')

		elif (line == 'rescan'):
			available_actions = common.scan_actions(V)

		elif (line == 'save'):
			print('input name to save this sequence under')
			line = input("#: ")
			fname = line+'.seq'
			common.save(fname, sequence)
			print('save OK!\n')

		elif (line == 'load'):
			allfilenames = files_in_folder('./sequences/')
			filenames = []
			for x in range(len(allfilenames)): # ignore everything but .seq files
				if (splitext(allfilenames[x])[1] == '.seq'):
					filenames.append(allfilenames[x])

			if (len(filenames) == 0):
				print('no saved sequences present\n')
				continue
			print('available sequence files:\n')
			for x in range(len(filenames)):
				print(splitext(basename(filenames[x]))[0])
			print('')
			while (1):
				print('input one of the above file names to load it')
				line = input("#: ").strip()
				line = line+".seq"
				if (exists("./sequences/"+line)):
					sequence = common.load(line)
					print('load OK!\n')
					break
				else:
					print('file not found, try again')

		elif (line[:3]=='no '): # remove from sequence
			parts = line.split(' ')
			if (len(parts) < 2):
				print("provide at least one sequence line number to remove")
			else:
				numbers = parts[1:]
				for n in numbers:
					try:
						n = int(n)
					except Exception as e:
						print('cannot parse as integer: ', n)
						continue
					else:
						if (n in sequence):
							print('removed line ', n)
							del sequence[n]
						else:
							print('cannot remove '+str(n)+": no such line")
			print(' ')

		# not a special command
		else:
			
			# if it has a question mark - it's action-specific help
			if (line[-1]=='?'): 
				line = line[:-1]
				if (line in available_actions):
					module = common.arm_action(line)
					about = getattr(module, 'about')
					print(about)
				else:
					print('no such action - cannot display help')
				print('')


			# if it's just one word w/o sequence num - execute
			elif (len(line.split(' ')) == 1): 
				if (line in available_actions):
					t = prepare_sequence_action(line)
					run_action(t)
					
				else:
					print('no such action - cannot execute')
				print('')

			# else it is a sequence entry
			else: 
				parts = line.split(' ')
				seq_number = -1
				try:
					seq_number = int(parts[0])
				except Exception as e:
					print('cannot parse sequence number as integer from 0 to '+str(SEQ_MAX)+': ', parts[0])
					continue
				seq_action_name = parts[1].strip()
				if (seq_number > SEQ_MAX):
					print('sequence number exceeds maximal ('+str(SEQ_MAX)+'):', seq_number)
				elif (seq_number < 0):
					print('sequence number should be zero or positive:', seq_number)
				elif (seq_action_name not in available_actions):
					print('no such action - cannot add to sequence')
				else:
					o = prepare_sequence_action(seq_action_name)
					sequence[seq_number] = o
					print('OK: ', seq_number, '-->', o)
				print('')
	print('\ngoodbye!\n')
	return


#-------------#-------------#-------------#-------------#-------------#-------------#
#GLOBALS

CATCHFAILS = True
SEQ_MAX = 999
V = True

status = None
available_actions = list()
status = sequence_status()
sequence = dict()

#-------------#-------------#-------------#-------------#-------------#-------------#
#RUNTIME

if (__name__ == '__main__'):

	v(V, '\nlaunching MESS...')

	available_actions = common.scan_actions(V)
	main()
	