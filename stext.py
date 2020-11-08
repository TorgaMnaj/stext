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
##:       - chapter                                                           #
#::       - topic in chapter                                                  #
#<:      - appendix begin                                                     #
#:>      - appendix end                                                       #
#@       - link                                                               #
# TODO:  - todo                                                               #
```      - beggining of multi line code                                       #
```      - end of multi line code                                             #
#>>>     - single line code                                                   #
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
	elif sys.argv[1] == "-r":
		filename = sys.argv[2]
		index_file(filename)
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


def index_file(filename):
	"""
	Analyzes given file.
	:param filename:
	:type filename:
	:return:
	:rtype:
	"""
	with open(filename, "r") as r:
		filelines = r.read().splitlines()
		filelines = list(enumerate(filelines, start=1))
	# get just indexing text:
	formtext = []
	reading = False
	for i in filelines:
		if reading:
			formtext.append(i)
		if i[1].startswith("#IB:"):
			reading = True
		elif i[1].startswith("#IE:"):
			reading = False
	# get indexes:
	todos = []
	links = []
	blockcodecodes = []
	linecodes = []
	apendixes = []
	chapters = []
	#
	ch = []
	code = []
	apdx = []

	#
	for i in formtext:
		# detecting todo:
		if "# todo:" in i[1].lower():
			todos.append(i)
		# links detection:
		if "#@ " in i[1]:
			links.append(i)
		# single code detection:
		if "#>>>" in i[1]:
			linecodes.append(i)
		# blockcode detection:
		if "```" in i[1] and not code:
			code.append(i)
		elif code and i[1] != "```":
			code.append(i)
		elif "```" in i[1] and code:
			code.append(i)
			blockcodecodes.append(code)
			code = []
		# appendix detection:
		if "#<:" in i[1]:
			apdx.append(i)
		elif apdx:
			apdx.append(i)
		if "#:>" in i[1]:
			apendixes.append(apdx)
			apdx = []
		# chapters detection
		if "##:" in i[1]:
			if ch:
				chapters.append(ch)
				ch = []
			ch.append(i)
		elif "#<:" in i[1] or "#IE:" in i[1]:
			if ch:
				chapters.append(ch)
				ch = []
		elif ch:
			ch.append(i)

	# topics detection:
	alltopics = []
	if chapters:
		chaptertopics = []
		for chapter in chapters:
			topic = []
			for chline in chapter:
				if "#:: " in chline[1]:
					if topic:
						chaptertopics.append(topic)
						topic = []
					topic.append(chline)
				elif topic:
					topic.append(chline)
			chaptertopics.append(topic)
			alltopics.append(chaptertopics)
			chaptertopics = []
	else:
		topic = []
		for chline in formtext:
			if "#:: " in chline[1]:
				if topic:
					alltopics.append(topic)
					topic = []
				topic.append(chline)
			elif topic:
				topic.append(chline)
		if topic:
			alltopics.append(topic)
	return todos, links, blockcodecodes, linecodes, apendixes, chapters, alltopics


print(str(index_file("./pytests/test_text.st")))
