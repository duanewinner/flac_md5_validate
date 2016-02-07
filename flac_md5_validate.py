#!/usr/local/bin/python3

import hashlib
import os
import sys
from collections import OrderedDict

def read_textfile_as_param():
    """ Function to open a file as an argument when launching program.
    Capture common errors and exit with error code of 1,
    printing friendly messages.
    """
    
    try:
        filename = sys.argv[1]
        try:
            openfile = open(filename, 'r')
            try:
                return openfile.read()
            except UnicodeDecodeError:
                print("\nFile \"{0}\" is not a text file.\n".format(filename))
                sys.exit(1)
        except FileNotFoundError:
            print("\nFile \"{0}\" could not be found.\n".format(filename))
            sys.exit(1)
        except PermissionError:
            print("\nPermission denied trying to read file \"{0}\".\n".\
                  format(filename))
            exit(1)
        except IsADirectoryError:
        	print("\n\"{0}\" is a directory, not a file.\n".format(filename))
        	exit(1)
    except IndexError:
        print("\nUsage: ./final.py [path-to/]<filename>\n")
        sys.exit(1)


directory = os.path.dirname(sys.argv[1])

manifest = []
for track in read_textfile_as_param().splitlines():
	manifest.append((track.split()[1].replace('*',''),track.split()[0]))


errors = False
for track in manifest:
	try:
		md5sum = hashlib.md5(open(directory + "/" + track[0],'rb').read()).hexdigest()
	except FileNotFoundError:
		print("{0} is missing!".format(track[0]))
		errors = True
	else:
		if md5sum == track[1]:
			print("{0} passes, ready to burn".format(track[0]))
		else:
			print("{0} md5 checksum does not match!".format(track[0]))
			errors = True
if errors == False:
	print("-" * 50 + "\n" + "No errors found; ready to burn!")
else:
	print("-" * 50 + "\n" + "Errors found!")

