#!/usr/bin/env python3
# Copyright (c) 2020 Jan Magrot

"""
Modules creates and analyzes .st files.
"""

import sys

usage = """
Usage: stext.sh
-c filename	        Create new .stx file
-r filename 		Read .stx files menu
 filename		Read .stx files menu
-ch filename		Show .stx chapters
-t filename		Show .stx topics (with chapter arg precended shows only specific chapters topics)
-code filename		Show .stx code snipets (with chapter arg precended shows only specific chapters snipets)
-a filename		Show .stx appendix, when title provided, shows specific appendix
-links filename		Show .stx links
-ref filename           Reformat and reindex file
"""

infilesyntax = """
###############################################################################
                                                                              #
                                                                              #
# .stx files syntax:                                                          #
##       - chapter                                                            #
#:       - topic in chapter                                                   #
#(       - appendix begin                                                     #
#)       - appendix end                                                       #
#@       - link                                                               #
# TODO:  - todo                                                               #
```      - beggining of multi line code                                       #
```      - end of multi line code                                             #
#>       - single line code                                                   #
                                                                              #
                                                                              #
###############################################################################
#IB: indexing begins:



#IE: indexing ends:
"""


def check_and_get_arguments():
	"""
	Checks arguments and chooses an action.
	:return:
	:rtype:
	"""
	if len(sys.argv) < 2:
		print("\nAt least one argument needed.")
		print(usage)
	elif sys.argv[1] == "-c":
		filename = sys.argv[2]
		create_file(filename)
	return True

def create_file(filename):
	"""
	Function for .st file creation.
	:return:
	:rtype:
	"""
	if "." in filename:
		filename = filename.split(".")[0]
	with open(filename + ".st", "w") as o:
		o.write("\n\t\t" + filename + "\n")
		o.write(infilesyntax)
	return True
