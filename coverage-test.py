#!/usr/bin/python
import re
import sys
from os import listdir
from os.path import isfile, join

TCOLOR_OKGREEN = '\033[92m'
TCOLOR_WARNING = '\033[93m'
TCOLOR_FAIL = '\033[91m'
TCOLOR_UNDERLINE = '\033[4m'
TCOLOR_ENDC = '\033[0m'

def get_unused_items(sourcetext, testtext):
	# Extract everything that can be used in source file
	functions = re.findall(r'\s.+: func ', sourcetext)
	functions += re.findall(r'\s.+: static func ', sourcetext)
	#functions += re.findall(r'\s.+: func ~.+?\s', sourcetext)
	#functions += re.findall(r'\s.+: static func ~.+?\s', sourcetext)	
	properties = re.findall(r'\s.+ ::=', sourcetext)
	operators = re.findall(r'\s+operator \S+', sourcetext)

	# Clean up results
	functions = [w.replace(' static func ','').replace(' func ','').replace(':','').strip() for w in functions]
	properties = [w.replace('::=','').strip() for w in properties]
	operators = [' ' + w.replace('operator','').strip() + ' ' for w in operators]

	# Eliminate whatever functions that are used:
	index = 0
	while index < len(functions):
		if testtext.find(functions[index]) > -1 or '_' in functions[index] or 'init' in functions[index] or '//' in functions[index] or '/*' in functions[index] or	'*/' in functions[index] or	'println' in functions[index]:
			del functions[index]
		else:
			index += 1

	# Eliminate whatever properties that are used:
	index = 0
	while index < len(properties):
		if testtext.find(properties[index]) > -1:
			del properties[index]
		else:
			index += 1

	# Eliminate whatever operators that are used:
	index = 0
	while index < len(operators):
		if testtext.find(operators[index]) > -1 or '[]' in operators[index]:
			del operators[index]
		else:
			index += 1

	# Eliminate duplicates
	seen = set(); functions = [x for x in functions if x not in seen and not seen.add(x)]
	seen = set(); properties = [x for x in properties if x not in seen and not seen.add(x)]
	seen = set(); operators = [x for x in operators if x not in seen and not seen.add(x)]
	return (functions, properties, operators)


# Load source and corresponding test file
print(TCOLOR_UNDERLINE + 'ooc-kean test coverage tester 0.3' + TCOLOR_ENDC)
try:
	directory = sys.argv[1]
	files = [ f for f in listdir('source/'+directory+'/') if isfile(join('source/'+directory+'/',f)) ]
	for each in files:
		try:
			with open('source/'+directory+'/'+each) as sourcefile:
				sourcetext = sourcefile.read()		
			with open('test/'+directory+'/'+each.replace('.ooc','')+'Test.ooc') as testfile:
				testtext = testfile.read()

			(functions, properties, operators) = get_unused_items(sourcetext, testtext)
		except:
			print(TCOLOR_FAIL + "Could not find test for " + each + TCOLOR_ENDC)
			continue

		# Print to user
		results = functions + properties + operators
		if results:
			print(TCOLOR_WARNING + "=== Not used in " + each + ' ===' + TCOLOR_ENDC)
			print('\n'.join(results))
		else:
			print(TCOLOR_OKGREEN + "=== Complete coverage in " + each + " ===" + TCOLOR_ENDC)
			None
except:
	print(TCOLOR_FAIL + "Directory not found." + TCOLOR_ENDC)
