#!/usr/bin/env python3
import sys
import subprocess
import re
import pprint
import glob
import os
import random
import collections
import csv
import string
from pathlib import Path
import stanza

from parsing.import_tools import sentPysbd
from parsing.stanza_parser import (
    preparenlpconf,
    load_config,
    parseciep
)

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

USAGE = './ud-stanza-ciep.py -s <source_directory> -t <target_directory> -l <language> -m <metadata_directory> -p <alternative sentence splitter> [-h] '

def build_parser():

    parser = argparse.ArgumentParser(description='ud-stanza-ciep - build beautiful CoNLL-U files')


    parser.add_argument('-s', '--source', required=True, help='Source for raw texts, must be dir/dir/dir')
    parser.add_argument('-t', '--target', required=True, help='Target destination for processed texts')
    parser.add_argument('-m', '--metadata', required=True, help='Target destination for metadata')
    parser.add_argument('-l', '--model', required=True, help='Language model e.g., en for English, zh for Chinese. Use mine for custom models.')
    parser.add_argument('-p', '--pipeline', required=True, type=str, help='NLP pipeline processors, separated by comma e.g. tokenize,lemma,mwt,pos,depparse,ner')
    parser.add_argument('-c', '--miniciep', required=False, help='Create miniciep+')
    parser.add_argument('-g', '--gpu', required=False, help='Use gpu? True/False')
    parser.add_argument('-n', '--config', required=False, help='config file')
    parser.add_argument('-x', '--ssplitter', required=False, help='Alternative sentence splitter')

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
    gpu = args.gpu
    '''Check arguments'''    
    if check_args(args) is False:
     sys.stderr.write("There was a problem validating the arguments supplied. Please check your input and try again. Exiting...\n")
     sys.exit(1)
    '''Unknown function, I'll check it later''' 
    start_time = time.time()
    import platform
    '''Prepare config for the NLP pipeline'''
    if args.config is None:
        config = preparenlpconf(ud,args.pipeline)
    elif args.config == "gsdluw":
        config = {
                        # Language code for the language to build the Pipeline in
                        # Processor-specific arguments are set with keys "{processor_name}_{argument_name}"
                        # You only need model paths if you have a specific model outside of stanza_resources
                        'lang': 'ja',
                        'processors': 'tokenize,depparse,pos,lemma',
	                    'tokenize_model_path': "/stanza_resources/ja/tokenize/gsdluw.pt",
                        #'mwt_model_path' : "",
	                    'pos_model_path': "/stanza_resources/ja/pos/gsdluw_charlm.pt" ,
	                    'lemma_model_path': "/stanza_resources/ja/lemma/gsdluw_nocharlm.pt",
	                    'depparse_model_path': "/stanza_resources/ja/depparse/gsdluw_charlm.pt" ,
                        'pos_pretrain_path': "/stanza_resources/ja/pretrain/conll17.pt",
                        'depparse_pretrain_path': "/stanza_resources/ja/pretrain/conll17.pt",
			            'pos_charlm_forward_path':"/stanza_resources/ja/forward_charlm/conll17.pt",
			            'pos_charlm_backward_path':"/stanza_resources/ja/backward_charlm/conll17.pt",
                        }
    elif isinstance(args.config, str):     # We expect this to be a path to a JSON file
        config = load_config(args.config)
    print(config)
    nlp = stanza.Pipeline(**config, logging_level="DEBUG",allow_unknown_language=True,use_gpu=gpu)

    for filename in sorted(glob.glob(args.source+'/*.txt')):
        file_content = open(filename, encoding='utf-8').read()
        print("Reading: " + filename)
        '''Extract metadata'''
        #Handle BOM
        header = re.findall(r'@.*', file_content.replace('\ufeff', ''))
        try:
            header.remove('@endheader')
        except:
            pass
        metadata = open(args.metadata + "/" + Path(filename).stem + ".metadata", "w+")
        if header:
            title = Path(filename).stem.split("_")[0]
            metadata.write("<text id=\"" + title + "\" ")
            for feature in header:
                value = feature.split('=')
                try:
                    metadata.write(re.sub('^@', '', value[0].strip()) + "=\"" + value[1].strip() + "\" ")
                except:
                    pass
        else:
            '''or extract metadata from filename...'''
            lang = Path(filename).stem.split("_")[1]
            title = Path(filename).stem.split("_")[0]
            metadata.write("<text id=\"" + title + "\" ")
            metadata.write("origtitle=\"" + title + "\" language=\"" + lang + "\" ")
        metadata.write(">")
        metadata.close()
        print("Starting parser...")
        if args.ssplitter == "pysbd":
            #Rewrite the NLP pipeline
            nlp = stanza.Pipeline(**config, logging_level="DEBUG", allow_unknown_language=True, use_gpu=gpu, tokenize_no_ssplit=True)
            #Alternate sentence splitting
            file_content = sentPysbd(lang,file_content)

        parseciep(nlp, file_content, filename, args.target, args.miniciep)
    print("--- %s seconds ---" % (time.time() - start_time))
    print("Done! Happy corpus-based typological linguistics!\n")

if __name__ == "__main__":
    main()
    sys.exit(0)

