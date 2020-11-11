#!/usr/bin/env python3
# Copyright (c) 2020 Jan Magrot

"""
Modules creates and analyzes .st files.
"""

import sys

linelength = 77
pagelength = 5
bline = "#" * (linelength + pagelength)

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

syntax = \
    "\n\n" + bline + """

# SYNTAX:

##:       - chapter
#::       - topic in chapter
#<:      - appendix begin
#:>      - appendix end
#@       - link
# TODO:  - todo
```      - beggining of multi line code
```      - end of multi line code
#>>>     - single line code

""" + bline + "\n"

index = """

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
        o.write(syntax)
        o.write(index)
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


def reformat_file(filename):
    """
    Function for reformating given file,
    according to .st syntax.
    :param filename:
    :type filename:
    :return:
    :rtype:
    """
    with open(filename, "r") as r:
        filelines = r.read().splitlines()

    # get just indexing text:
    formtext = []
    reading = False
    for i in filelines:
        if i.startswith("#IB:"):
            reading = True
        if reading:
            formtext.append(i)
        elif i.startswith("#IE:"):
            reading = False

    newfile = []
    for i in formtext:
        if "todo:" in i.lower():
            r = i.lower().split("todo:")[1]
            i = "# TODO:" + r.lower()
        newfile.append(i)
    filelines = []
    for i in newfile:
        if "##: " in i:
            i = i.upper()
        filelines.append(i)
    newfile = []
    for i in filelines:
        if "#:: " in i:
            i = i.title()
        newfile.append(i)
    retfile = []
    empty = "n"
    # formating empty lines:
    for i in newfile:
        if i == "":
            if empty != "":
                retfile.append(i)
        else:
            retfile.append(i)
        empty = i
    rfile = []
    for i in retfile:
        if "##:" in i or "#<:" in i:
            for _ in range(3):
                rfile.append("")
        elif "#::" in i:
            for _ in range(2):
                rfile.append("")
        rfile.append(i)
    # Write table of content to file:
    retfile = ""
    retfile += syntax
    for i in rfile:
        if i.startswith("#IB: "):
            for _ in range(2):
                retfile += "\n"
            todos, links, blockcodecodes, linecodes, apendixes, chapters, alltopics = index_file(filename)
            content = get_chapters_topics_appendixes_string(apendixes, chapters, alltopics)
            retfile += content
            for _ in range(3):
                retfile += "\n"
            retfile += bline + "\n\n\n"
        retfile += i + "\n"
    return retfile


def get_chapters_topics_appendixes_string(apendixes, chapters, alltopics):
    """
    Function that returns pretty printed chapters if presented,
    topics and appendixes for stdout.
    :return:
    :rtype:
    """
    out = "\nTABLE OF CONTENTS:\n\n"
    if chapters:
        for chapt in chapters:
            # get chapters:
            pre = chapt[0][1].split("##: ")[1]
            add = (linelength - len(pre)) * "."
            ll = str(chapt[0][0])
            post = str((pagelength - len(ll)) * ".") + ll
            out += str(pre + add + post)
            out += "\n"
            # get topics:
            for toplist in chapt:
                if toplist[1].startswith("#::"):
                    tpre = toplist[1].split("#:: ")[1]
                    if tpre[0] == " ":
                        tpre = tpre[1:]
                    pre = " " + tpre
                    add = (linelength - len(pre)) * "."
                    ll = str(toplist[0])
                    post = str((pagelength - len(ll)) * ".") + ll
                    out += str(pre + add + post)
                    out += "\n"
            out += "\n"
    else:
        # get topics:
        for toplist in alltopics:
            if toplist[0][1].startswith("#::"):
                tpre = toplist[0][1].split("#:: ")[1]
                if tpre[0] == " ":
                    tpre = tpre[1:]
                pre = " " + tpre
                add = (linelength - len(pre)) * "."
                ll = str(toplist[0][0])
                post = str((pagelength - len(ll)) * ".") + ll
                out += str(pre + add + post)
                out += "\n"
        out += "\n"

    if apendixes:
        out += "\nAPENDIXES:\n\n"
        for ap in apendixes:
            tpre = ap[0][1].split("#<: ")[1]
            if tpre[0] == " ":
                tpre = tpre[1:]
            pre = " " + tpre
            add = (linelength - len(pre)) * "."
            ll = str(ap[0][0])
            post = str((pagelength - len(ll)) * ".") + ll
            out += str(pre + add + post)
            out += "\n"
    return out
