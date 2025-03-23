#!/usr/bin/env python3
import sys
import re
import glob
from pathlib import Path
import stanza
import argparse

from parsing.stanza_parser import (
    preparenlpconf,
    load_config,
    parseciep, parsealtciep, parsealtminiciep, parseminiciep
)

import time
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
    parser.add_argument('-c', '--miniciep', action='store_true', help='Create miniciep+')
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
        if args.miniciep:
             if Path(args.target + "/" + "mini" + "/" + Path(filename).stem + ".conllu").exists():
              print(args.target + "/" + "mini" + "/" + Path(filename).stem + ".conllu" + " already exists, skipping to next book")
             else:
              nlp = stanza.Pipeline(**config, allow_unknown_language=True)
              if args.ssplitter == "pysbd":
                print("Ok, using pysbd as an alternative sentence splitter...")
                # Rewrite the NLP pipeline
                nlp = stanza.Pipeline(**config,allow_unknown_language=True, tokenize_no_ssplit=True)
                # Alternate sentence splitting
                parsealtminiciep(nlp, file_content, filename, args.target, args.model)
              else:
                parseminiciep(nlp, file_content, filename, args.target)
        else:
              if Path(args.target + "/" + "full" + "/" + Path(filename).stem + ".conllu").exists():
                print(args.target + "/" + "full" + "/" + Path(filename).stem + ".conllu" + " already exists, skipping to next book")
              else:
               nlp = stanza.Pipeline(**config, allow_unknown_language=True)
               if args.ssplitter == "pysbd":
                print("Ok, using pysbd as an alternative sentence splitter...")
                # Rewrite the NLP pipeline
                nlp = stanza.Pipeline(**config, allow_unknown_language=True, tokenize_no_ssplit=True)
                # Alternate sentence splitting
                parsealtciep(nlp, file_content, filename, args.target, args.model)
               else:
                parseciep(nlp, file_content, filename, args.target)
    print("--- %s seconds ---" % (time.time() - start_time))
    print("Done! Happy corpus-based typological linguistics!\n")

if __name__ == "__main__":
    main()
    sys.exit(0)

