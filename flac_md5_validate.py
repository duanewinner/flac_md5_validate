#!/usr/local/bin/python3

import hashlib
import mimetypes
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
                directory = os.path.dirname(sys.argv[1])
                return (openfile.read(), directory)
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

def validate_manifest(manifest_file, manifest_directory):
    manifest = []
    for track in manifest_file.splitlines():
        manifest.append((track.split()[1].replace('*',''),track.split()[0]))

    errors = False
    for track in manifest:
        try:
            md5sum = hashlib.md5(open(manifest_directory + "/" + track[0],'rb').read()).hexdigest()
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
        return(("-" * 50 + "\n" + "No errors found; ready to burn!\n" + "-" * 50), 0)
    else:
        return(("-" * 50 + "\n" + "Errors found!\n" + "-" * 50), 1)

def check_for_flac():
    return(os.path.isfile("/usr/local/bin/flac"))

def burn_to_disc():
    discs = set()
    for line in file[0].splitlines():
        discs.add((line.split()[1].replace('*',''))[:-8])
    print("-" * 50 + "\nYou will need {0} blank CD-R discs.".format(max(discs)[-1]))
    while True:
        confirm = input("Enter 'c' to continue, or 'q' to quit: ")
        if confirm.lower() == 'q':
            exit(0)
        elif confirm.lower() == 'c':
            input("-" * 50 + "\nInsert the first disc, then hit 'c' to continue...")
            for disc in sorted(discs):
                print("Complete. Label the ejected disc as {0}".format(disc))
                if disc[-1] < max(discs)[-1]:
                    while True:
                        confirm = input("-" * 50 + "\nInsert the next disc then hit 'c' to continue.\n(Or 's' to skip this disc. ")
                        break
                else:
                    print("-" * 50 + "\nFinished!\n" + "-" * 50 )
                    exit(0)


if __name__ == '__main__':
    file = read_textfile_as_param()
    validation_results = (validate_manifest(file[0], file[1]))
    print(validation_results[0])

    if validation_results[1] == 1:
        exit(1)
    else:
        if check_for_flac():
            print("\"flac\" appears to be installed.")
            while True:
                burn_confim = input("Would you like to burn now with flac and drutil? (y/n): ")
                if burn_confim.lower() == 'n':
                    exit(0)
                elif burn_confim.lower() == 'y':
                    burn_to_disc()
                    exit(0)


