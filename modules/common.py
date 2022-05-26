#-------------#-------------#-------------#-------------#-------------#-------------#
#IMPORTS

import os
from os import listdir
from os.path import splitext
from sys import platform
from importlib import import_module as imp
import json



#-------------#-------------#-------------#-------------#-------------#-------------#
#CLASS DEFINITIONS

'''
holds information about sequence's current path, current file selection, etc.
is passed to action modules' functions as argument, they can then modify it
'''
class sequence_status():
	def __init__(self):
		self.path = "unset"
		self.selection = list()

	def __str__(self):
		out = ""
		out+= ('system status:')
		out+= ('\n  working path:   '+ self.path)
		out+= ('\n  files selected: '+ str(len(self.selection)) + " (run 's' to see the list)")
		out+= ('\n')
		return out


'''
a record of a particular action with particular parameters
stored in the sequence dictionary under a unique sequence number
'''
class sequence_action():

	def __init__(self, n="", p=""):
		self.name = n # has to be the same as action entry
		self.params = p # parameters further read by the action's module when launched, name-value dictionary

	def __str__(self):
		out = self.name
		if (len(self.params)>0):
			out += " ("
			for x in self.params:
				out += str(x)+":"+str(self.params[x])+", "
			out = out[:-2]+")"
		return out

	def serialize(self):
		d = dict()
		d['name'] = self.name
		d['params'] = self.params
		return d

	def deserialize(self, dict):
		self.name = dict['name']
		self.params = dict['params']

'''
makes a sequence number (0...SEQ_MAX, int) into a string taking exactly 4 characters
'''
def format_seq_num_str(arg):
	return str(arg)+' '*(4-len(str(arg)))


#-------------#-------------#-------------#-------------#-------------#-------------#
#FUNCTION DEFINITIONS 

'''
verbose-flag-aware printing
'''
def v(verbose, contents):
	if verbose:
		print(contents)

'''
returns reference to action module by name
'''
def arm_action(name):
	mod = imp("actions."+name)
	return mod

'''
scans the action folder for valid action modules
'''
def scan_actions(V):

	available_actions = []
	v(V,'scanning actions folder...')
	files = listdir("./actions/")
	ignore = ['__init__', '__pycache__', 'helper', 'template', '.DS_Store']
	for f in files:
		module = None
		parts = splitext(f)
		name = parts[0]
		if (name in ignore):
			v(V, 'ignoring: '+name)
			continue
		try:
			module = arm_action(name)
		except Exception as e:
			print('saw potential action file, could not arm: '+ name+ ' | ',e)
			continue
		else:
			try:
				# check metadata integrity - to be sure stuff is here
				action_about = getattr(module, 'about')

			except Exception as e:
				print('saw potential action file, could not read metadata: '+ name)
				continue
			else:
				available_actions.append(name)
				v(V,'successfully loaded action: '+name)
	print('done!\n')
	return available_actions

'''
clears console screen
'''
def cls():
	if platform == 'win32' or platform=='msys' or platform=='cygwin':
		os.system('cls')
	else:
		os.system('clear')

'''
saves given sequence to json file
'''
def save(fname, sequence):
	fh = open('./sequences/'+fname, 'w')
	out_dict = dict()
	for number in sequence:
		out_dict[number] = sequence[number].serialize()
	out_json = json.dumps(out_dict)
	fh.write(out_json)
	fh.close()

'''
loads a sequence from a given json file
'''
def load(fname):
	fh = open('./sequences/'+fname, 'r')
	in_json = fh.read()
	fh.close()
	in_dict = json.loads(in_json)
	sequence = dict()
	for number in in_dict:
		t = sequence_action()
		t.deserialize(in_dict[number])
		sequence[int(number)] = t
	return sequence