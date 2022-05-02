#!/bin/python

import re
import os
import sys
import json
import subprocess


DEF_FILE = '.2lane.info'
DIRECTIVE_TEMPLATE = '<!-- 2L {body} -->'
TYPO_WARNING_FINDER = re.compile('\W2L\W', re.IGNORECASE)
MESSAGE_TEMPLATE = '** 2lanemdr {kind} on {filename}:{linenumber} "{message}"'

def parseDirective(line, wrcs):
    """
        Return (kind, target):
            ('endif', None)
            ('if', <fn>)
            ('elif', <fn>)
            (None, None)
    """
    if line == DIRECTIVE_TEMPLATE.format(body='ENDIF'):
        return ('endif', None)
    else:
        for fn in wrcs.keys():
            if line == DIRECTIVE_TEMPLATE.format(body='IF %s' % fn):
                return ('if', fn)
            elif line == DIRECTIVE_TEMPLATE.format(body='ELIF %s' % fn):
                return ('elif', fn)
        #
        return None, None


def mkFiles(src, prescr, warner, errorer):
    """
    Return a list with the path to all files created
    """
    inContents = [
        li.replace('\n', '')
        for li in open(src).readlines()
    ]
    # open files
    oFiles = {
        fn: open(fp, 'w')
        for fn, fp in prescr.items()
    }
    # cursor setting
    writing = {
        fn: True
        for fn in oFiles.keys()
    }

    # process lines
    for lineNumber, line in enumerate(inContents):
        # directive or content line?
        directive, dTarget = parseDirective(line, writing)
        if directive is not None:
            # validate and process
            if directive == 'endif':
                if sum(int(c) for c in writing.values()) != 1:
                    errorer('Misplaced ENDIF', lineNumber)
                else:
                    for fn in writing.keys():
                        writing[fn] = True
            elif directive == 'if':
                if sum(int(c) for c in writing.values()) != len(writing):
                    errorer('Misplaced IF', lineNumber)
                else:
                    for fn in writing.keys():
                        writing[fn] = fn == dTarget
            elif directive == 'elif':
                if sum(int(c) for c in writing.values()) != 1:
                    errorer('Misplaced ELIF', lineNumber)
                elif writing[dTarget]:
                    errorer('Repeated target in ELIF', lineNumber)
                else:
                    for fn in writing.keys():
                        writing[fn] = fn == dTarget
            else:
                errorer('Unknown directive', lineNumber)
        else:
            #
            if TYPO_WARNING_FINDER.search(line):
                warner('check line', lineNumber)
            # write serially on all active cursors
            for fn, fh in oFiles.items():
                if writing[fn]:
                    fh.write('%s\n' % line)

    # close files
    for fn, fh in oFiles.items():
        fh.close()

    return [fp for fp in prescr.values()]


if __name__ == '__main__':

    if os.path.isfile(DEF_FILE):
        defs = json.load(open(DEF_FILE))
        files = defs.get('sources', {})
        #
        allCreatedFiles = []
        #
        for origF, dests in files.items():

            def warner(msg, intLineno):
                wmsg = MESSAGE_TEMPLATE.format(
                    kind='WARNING',
                    filename=origF,
                    linenumber=intLineno+1,
                    message=msg,
                )
                print(wmsg)

            def errorer(msg, intLineno):
                emsg = MESSAGE_TEMPLATE.format(
                    kind='ERROR',
                    filename=origF,
                    linenumber=intLineno+1,
                    message=msg,
                )
                print(emsg)
                sys.exit(1)

            createdFiles = mkFiles(origF, dests, warner=warner, errorer=errorer)
            allCreatedFiles += createdFiles

    # we git add the created files
    subprocess.call(['git', 'add'] + allCreatedFiles)
