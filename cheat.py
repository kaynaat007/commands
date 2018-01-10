import sys
import os
try:
	command = sys.argv[1]
except IndexError: 
     print ('Please provide name of the command to view cheat sheet')

def read(command):
   path_to_command_file = os.path.join(os.path.dirname(__file__), 'texts', command + '.txt' )
   with open(path_to_command_file, 'r') as f:
         print( f.read() )
	 
read(command)





