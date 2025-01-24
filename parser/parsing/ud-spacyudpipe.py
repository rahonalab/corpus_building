#!/usr/bin/env python3
import sys
import subprocess
import re
import pprint
import glob
import os
import random
import unicodedata
import collections
import csv
import string
import nltk.data
import spacy
import spacy_udpipe
import nltk
import pyconll
import pyconll.util




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

USAGE = './ud-parser.py <source_directory> <target_directory> [-h] \n [--shuffle | --parse PUNKT_LANG UD_LANG ] \n [--analyze UD_SYN_REL'

def build_parser():

    parser = argparse.ArgumentParser(description='ud-ciep - build beautiful CoNLL-U files, analyze data from CIEP raw data and UD treebank')


    parser.add_argument('source',help='Source for raw texts, must be dir/dir/dir')
    parser.add_argument('target',help='Target destination for processed texts')
    parser.add_argument('-p', '--parse', nargs=2,  help='Parse CIEP texts and print out conllu files: specify punk language model, ud model')
    parser.add_argument('-a', '--analyze', nargs='*', help='Analyze CIEP: specify UD syntactic relation')

    return parser


def check_args(args):
    '''Exit if required arguments not specified'''
    check_flags = {}

import unicodedata, re
all_chars = (unichr(i) for i in range(0x110000))
control_chars = ''.join(map(chr, list(range(0,32)) + list(range(127,160))))
control_char_re = re.compile('[%s]' % re.escape(control_chars))

def sanitize(s):
    return unicodedata.normalize('NFC', control_char_re.sub(' ', s))

def sentencesplitlang(file_content):
    from nltk.tokenize import sent_tokenize
    doc = sanitize(re.sub(r'(?m)^\@.*\n?',' ',file_content.replace('’', '\'').replace('‘', '\'')).replace('…',' ... ').replace('«',' " ').replace('»',' " ').replace('<BLOCK>',' '))
    sentences=enumerate(sent_tokenize(doc,language=punkt),1)
    return sentences

def loadmodel(model):
    try: 
        nlp = spacy_udpipe.load(model, ignore_tag_map=True)
        return nlp
    except:
        print(model+" not found. I'll try to download it...")
        try:
            spacy_udpipe.download(model)
            nlp = spacy_udpipe.load(model, ignore_tag_map=True)
            return nlp
        except:
            custom = input("Please insert the path to the custom model:")
            nlp = spacy_udpipe.load_from_path(lang=model,
                                  path=custom,
                                  meta={"description": "Custom model"})
            return nlp


def udparser(nlp,sentences,conllufile,newdoc):
    for sentence in sentences:
        print(sentence)
        conllufile.write("# sent_id = "+newdoc+"-s"+str(sentence[0])+"\n")        
        conllufile.write("# text = "+sentence[1].replace('\n', '')+"\n")
        for token in nlp(sentence[1]):
            conllufile.write(str(token.i+1)+"\t"+token.text+"\t"+token.lemma_+"\t"+token.pos_+"\t"+token.tag_+"\t"+'_'+"\t"+str(token.head.i+1)+"\t"+token.dep_+"\t"+'_'+"\t"+'_\n')
        conllufile.write("\n")
    conllufile.close() 

def udanalyzer(conllufile,countwriter):
    conllu = pyconll.load_from_file(conllufile)
    for sentence in conllu:
        left = {}
        right = {}
        for token in sentence:
            #Most of the time, in the token itself...
            if token.deprel in args.analyze:
                if token.deprel not in left:
                    left[token.deprel] = {}
                if token.deprel not in right:
                    right[token.deprel] = {}
                #Head is on the left
                if int(token.id) > int(token.head):
                    #collect token
                    left[token.deprel][token.id]= token
                #Head is on the right
                if int(token.id) < int(token.head):
                    #collect token
                    right[token.deprel][token.id]= token
        for syntacticrel in args.analyze:
            if syntacticrel in left:
                for ident,token in left[syntacticrel].items():
                    for x in sentence:
                        if token.head == x.id:
                            head = x
                        hmLength = abs(int(token.id)-int(token.head))
                    countwriter.writerow(['X-'+syntacticrel,head.deprel,token.deprel,head.form,token.form,head.lemma,token.lemma,head.upos,token.upos,hmLength,sentence.id,os.path.basename(conllufile).split('.')[0],conllu.__len__()])
            if syntacticrel in right:
                for ident,token in right[syntacticrel].items():
                    for x in sentence:
                        if token.head == x.id:
                            head = x
                        hmLength = abs(int(token.id)-int(token.head))
                    countwriter.writerow([syntacticrel+'-X',token.deprel,head.deprel,token.form,head.form,token.lemma,head.lemma,token.upos,head.upos,hmLength,sentence.id,os.path.basename(conllufile).split('.')[0],conllu.__len__()])
    return 


def header(file_content,conllufile):
    '''Identify header'''
    header = re.findall(r'@.*',file_content)
    '''Beginning of file'''
    conllufile.write("# newdoc id ")
    '''Format and print header: we just take origtitle and language, and build a newdoc id accordingly'''
    for feature in header:
        if re.compile("@origtitle").search(feature):
                origtitle = feature.split('=')
    newdoc = origtitle[1].split(' ')[0]+origtitle[1].split(' ')[1]+'_'+origtitle[1].split(' ')[4]+origtitle[1].split(' ')[5]
    conllufile.write("= "+newdoc+"\n")
    return(newdoc)


def main():
    global debug
    global args
    global seppath
    global punkt
    global ud
    parser = build_parser()
    args = parser.parse_args()
    if args.parse:
        punkt = args.parse[0]
        ud = args.parse[1]

    seppath = '/'
    '''Check arguments'''    
    if check_args(args) is False:
     sys.stderr.write("There was a problem validating the arguments supplied. Please check your input and try again. Exiting...\n")
     sys.exit(1)
    '''Unknown function, I'll check it later''' 
    start_time = time.time()
    if args.parse:
        import platform
        if platform.system() == 'Windows':
            seppath = '\\'
            spacy.require_gpu()
            '''Try to load the model into the parser'''
        nlp = loadmodel(ud)
        for filename in sorted(glob.glob(args.source+'/*.txt')):
            file_content = open(filename, encoding='utf-8').read()
            print("Try to analyze: "+filename)
            conllufile= open(args.target+ud+"_"+args.source.split(seppath)[0]+".conllu","a+",encoding='utf-8') 
            #newdoc = filename.split(seppath)[3].split('.')[0]
            newdoc = os.path.basename(filename).split('.')[0]
            sentences=sentencesplitlang(file_content)
            udparser(nlp,sentences,conllufile,newdoc)
            conllufile.close()
    if args.analyze:
        csvfile = open(args.target+"report-"+args.source.split(seppath)[2]+".csv", 'a+', newline='',encoding='utf-8')    
        countwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
        countwriter.writerow(['order', 'relfirst', 'relsecond', 'tokenfirst', 'tokensecond', 'lemmafirst', 'lemmasecond', 'uposfirst', 'upossecond', 'hmLength', 'sentence', 'source', 'size'])
        for conllufile in sorted(glob.glob(args.source+'/*.conllu')):
            conllu = pyconll.load_from_file(conllufile)
            udanalyzer(conllufile,countwriter)
    print("--- %s seconds ---" % (time.time() - start_time))
    print("Done! Happy corpus-based typological linguistics!\n")

if __name__ == "__main__":
    main()
    sys.exit(0)

