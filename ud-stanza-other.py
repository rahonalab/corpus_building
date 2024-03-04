#!/usr/bin/env python3
import sys
import subprocess
import re
import pprint
import glob
import os
import random
import collections
import string
import inspect
import stanza
import logging
from pathlib import Path



from parsing.stanza_parser import (
    parseother,
    parseprepared,
    preparenlpconf
)
        

from parsing.import_tools import (
    importRSC
)

from parsing.clean_text import preparetext

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

USAGE = './ud-stanza-other.py -s <source_directory> -t <target_directory> -c <corpus> -l <language> -m <metadata_directory> [-h] '

def build_parser():

    parser = argparse.ArgumentParser(description='ud-stanza-other - build beautiful CoNLL-U files')


    parser.add_argument('-s', '--source', required=True, help='Source for raw texts, must be dir/dir/dir')
    parser.add_argument('-t', '--target', required=True, help='Target destination for processed texts')
    parser.add_argument('-m', '--metadata', required=False, help='Target destination for metadata (optional)')
    parser.add_argument('-l', '--model', required=True, help='Language model e.g., en for English, zh for Chinese. Use mine for custom models.')
    parser.add_argument('-p', '--processors', required=True, type=str, help='NLP pipeline processors, separated by comma e.g. tokenize,lemma,mwt,pos,depparse,ner')
    parser.add_argument('-c', '--corpus', required=True, type=str, help='Available format: txt (just basic cleaning); leipzig (Leipzig Corpora Collection); rsc (RSC vrt format)')

    return parser

def check_args(args):
    '''Exit if required arguments not specified'''
    check_flags = {}

def main():
    global debug
    global args
    global ud
    global NEWDOC
    parser = build_parser()
    args = parser.parse_args()
    ud = args.model
    corpus = args.corpus
    '''Check arguments'''    
    if check_args(args) is False:
     sys.stderr.write("There was a problem validating the arguments supplied. Please check your input and try again. Exiting...\n")
     sys.exit(1)
    '''Unknown function, I'll check it later''' 
    start_time = time.time()
    '''Prepare NLP pipeline config'''
    config = preparenlpconf(ud,args.processors)
    #Generic conllu
    if corpus == "conllu":
     print("Ok, parsing conllu files...")
     for filename in sorted(glob.glob(args.source+'/*.conllu')):
      print("Reading: "+filename)
      nlp = stanza.Pipeline(**config, logging_level="DEBUG", tokenize_pretokenized=True, tokenize_no_ssplit=True)
      from stanza.utils.conll import CoNLL
      #Import conllu into doc object
      text = CoNLL.conll2doc(filename)
      parseprepared(nlp,text,filename,args.target)
     return
    if corpus == "txt":
     nlp = stanza.Pipeline(**config, logging_level="DEBUG",allow_unknown_language=True,download_method=None)
     for filename in sorted(glob.glob(args.source+'/*.txt')):
      #Just parse the file as-is
      text = open(filename, encoding='utf-8').read()
      text = preparetext(text)
      parseother(nlp,text,filename,args.target)
     return
    if corpus == "leipzig":
     file_content = open(filename, encoding='utf-8').read()
     #Remove the annoying Leipzig format
     text = re.sub(r'\d+\t','',file_content)
     parseother(nlp,text,filename,args.target)
     return
    if corpus == "rsc":
     for filename in sorted(glob.glob(args.source+'/*.vrt')):
     #Check if file already exists
      if(os.path.isfile(args.target+Path(filename).stem+".conllu")):
       print(filename+" already parsed, next please...")
      else:
       file_content = open(filename, encoding='utf-8').read()
       print("Reading: "+filename)
       print("Starting parser...")
       #RSC is already tokenized and sentence splitted
       nlp = stanza.Pipeline(**config, logging_level="DEBUG", tokenize_pretokenized=True, tokenize_no_ssplit=True)
       #We overwrite existing metadata as RSC's metadata are better
       rsc, metadata = importRSC(file_content)
       '''extract metadata from metadata...'''
       metafile= open(args.metadata+Path(filename).stem+".metadata","w+")
       metafile.write("<text ")
       for k,v in metadata.items():
        metafile.write(k+"=\""+v+"\""+" ")
        metafile.write(">")
        metafile.close()
        print("Parsing "+filename+"\n")
        if rsc:
         parseprepared(nlp,rsc,filename,args.target)
        else:
         print("Document is empty, writing an empty conllu file")
         conllu = args.target+Path(filename).stem+".conllu"
       file_content.close()
      return	                    
    print(corpus+" is currently not supported")

if __name__ == "__main__":
    main()
    sys.exit(0)

