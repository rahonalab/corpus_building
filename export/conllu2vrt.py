#!/usr/bin/env python3
import sys
import subprocess
import re
import glob
import pyconll
from pathlib import Path
import os

try:
    import argparse
except ImportError:
    checkpkg.check(['python-argparse'])

import time
import socket

"""

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
"""

USAGE = './conllu2vrt.py -f path_to_conllu_files [-m path_to_metadata] -o path_to_output_vrt'

def build_parser():

    parser = argparse.ArgumentParser(description='conllu2vrt.py - Convert conllu texts to xmlized vrts')
    parser.add_argument('-c', dest="conllu", required=True, help='path_to_conllu_files')
    parser.add_argument('-m', dest="metadata", required=False, help='path_to_metadata')
    parser.add_argument('-x', dest="vrt", required=True, help='path_to_output_vrt')
    parser.add_argument('-a', dest="annotation", required=False, help='human ref annotation')

    return parser


def main():
    global debug

    parser = build_parser()
    args = parser.parse_args()

    '''Check arguments'''    
    if check_args(args) is False:
     sys.stderr.write("There was a problem validating the arguments supplied. Please check your input and try again. Exiting...\n")
     sys.exit(1)

    '''Unknown function, I'll check it later''' 
    start_time = time.time()
    '''Beginning of file'''
    vrtfile= open(args.vrt+Path(args.conllu).stem+".vrt","w+")
    print("Processing "+args.conllu)
    if args.metadata:
        '''Load metadata'''
        metadata= open(args.metadata+Path(args.conllu).stem+".metadata").read()
    else:
        '''If metadata are not available, build them from the filename'''
        metadata = "<text id=\""+Path(args.conllu).stem+"\">"
    vrtfile.write(metadata+"\n")
    '''Put conllu file with sentence boundaries'''
    conllu = pyconll.load_from_file(args.conllu)
    if args.annotation:
        with open(args.annotation) as csvfile:
            import csv
            from collections import defaultdict
            columns = defaultdict(list) # each value in each column is appended to a list 
            reader = csv.DictReader(csvfile,delimiter="\t",skipinitialspace=False)
            for row in reader: # read a row as {column1: value1, column2: value2,...}
                for (k,v) in row.items(): # go over each column name and value 
                    columns[k].append(v) # append the value into the appropriate list
            columns['propn'] = [x.strip(' ') for x in columns['propn']]
            propn = set(k.lower() for k in columns['propn'])
    for sentence in conllu:
        vrtfile.write("<s>\n")
        vrtfile.write("# sent_id = "+sentence.id+"\n")
        if sentence.text != None:
            sentenceconll = sentence.text.replace('>','-').replace('<','-')
            vrtfile.write("# text = "+sentenceconll+"\n")
        else:
            vrtfile.write("# text = "+""+"\n")
        for token in sentence: 
            if args.annotation:
                if token.form in columns['propn']: 
                    print("Annotating "+token.form)
                    token.misc['Reference'] = set()
                    token.misc['Reference'].add('Human')
            conll = token.conll().replace('>','-').replace('<','-')
            vrtfile.write(conll+"\n")
        vrtfile.write("</s>\n")
    vrtfile.write("</text>\n")
    vrtfile.write("\n")

    '''Close file'''
    vrtfile.close()

def check_args(args):
    '''Exit if required arguments not specified'''
    check_flags = {}

def exec_command(command):
    """Execute command.
       Return a tuple: returncode, output and error message(None if no error).
    """
    sub_p = subprocess.Popen(command,
                             shell=True,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
    output, err_msg = sub_p.communicate()
    return (sub_p.returncode, output, err_msg)


if __name__ == "__main__":
    main()
    sys.exit(0)

