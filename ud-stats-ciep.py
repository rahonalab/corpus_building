############ This script prints out comma-separated spreadsheet(s) (miniciep+_{token,sentence}) with the size of each book of miniciep+ in token and sentence ########
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
import io
import pyconll
from pathlib import Path
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

USAGE = './ud-stats.py <source_directory> <csv_file>'

def build_parser():

    parser = argparse.ArgumentParser(description='ud-stats-ciep.py: Stats for (mini)ciep+')


    parser.add_argument('source',help='Source for parsed conllu files')
    parser.add_argument('target',help='Target destination for csv files')

    return parser


def check_args(args):
    '''Exit if required arguments not specified'''
    check_flags = {}

def udtext(conllufile):
    conllu = pyconll.load_from_file(conllufile)
    #Get numbers of token
    token = 0
    nsubj = 0
    obj = 0
    iobj = 0
    for sent in conllu:
        token += sent.__len__()
        for tok in sent:
            if re.findall('nsubj.*', str(tok.deprel)):
                nsubj += 1
            if re.findall('obj.*', str(tok.deprel)):
                obj += 1
            if re.findall('iobj.*', str(tok.deprel)):
                iobj += 1
    return token, conllu.__len__(), nsubj, obj, iobj
    
def main():
    global debug
    global args
    global seppath
    parser = build_parser()
    args = parser.parse_args()
    '''Check arguments'''    
    if check_args(args) is False:
     sys.stderr.write("There was a problem validating the arguments supplied. Please check your input and try again. Exiting...\n")
     sys.exit(1)
    '''Unknown function, I'll check it later'''
    start_time = time.time()
    csvtoken = open(args.target+"/miniciep+_token.csv", 'w', newline='',encoding='utf-8')    
    tokenwriter = csv.writer(csvtoken, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
    tokenwriter.writerow(['Language', '100YearsSolitude', 'AAiW', 'Achterhuis', 'Alchemist', 'NomeRosa', 'Parfum', 'PetitPrince', 'TtLG', 'Zahir', 'Zorba','AnimFarm','Archer','Cholera','AnGarda','BealBocht','Cre','Narnia1','Run','Bulle'])
    csvsentence = open(args.target+"/miniciep+_sentence.csv", 'w', newline='',encoding='utf-8')    
    sentencewriter = csv.writer(csvsentence, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
    sentencewriter.writerow(['Language', '100YearsSolitude', 'AAiW', 'Achterhuis', 'Alchemist', 'NomeRosa', 'Parfum', 'PetitPrince', 'TtLG', 'Zahir', 'Zorba','AnimFarm','Archer','Cholera','AnGarda','BealBocht','Cre','Narnia1','Run','Bulle'])
    csvall = open(args.target+"/miniciep+_stats.csv", 'w', newline='',encoding='utf-8')    
    statswriter = csv.writer(csvall, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
    statswriter.writerow(['Language', 'Tokens', "Sentences", "nsubj", "obj", "iobj"])

    for lang in sorted(glob.iglob(args.source+"/**")):
        texts = []
        #Check if mini/ directory exists
        if os.path.isdir(lang+"/mini"):
            for conllu in sorted(glob.iglob(lang+"/mini/*.conllu")):
                print(conllu)
                token, sentence, nsubj, obj, iobj  = udtext(conllu)
                text = {"name": os.path.basename(conllu.split("_")[0]), "token": token, "sentence": sentence, "nsubj": nsubj, "obj": obj, "iobj": iobj}
                texts.append(text)
            #Write token size
            tokenrow = [os.path.basename(lang),0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
            for text in texts:
                if "100" in text["name"]:
                    tokenrow[1] = int(text["token"])
                if "AAiW" in text["name"]:
                    tokenrow[2] = int(text["token"])
                if "Achter" in text["name"]:
                    tokenrow[3] = int(text["token"])
                if "mist" in text["name"]:
                    tokenrow[4] = int(text["token"])
                if "Rosa" in text["name"]:
                    tokenrow[5] = int(text["token"])
                if "Parfum" in text["name"]:
                    tokenrow[6] = int(text["token"])
                if "Prince" in text["name"]:
                    tokenrow[7] = int(text["token"])
                if "TtLG" in text["name"]:
                    tokenrow[8] = int(text["token"])
                if "Zahir" in text["name"]:
                    tokenrow[9] = int(text["token"])
                if "Zorba" in text["name"]:
                    tokenrow[10] = int(text["token"])
                if "AnimFarm" in text["name"]:
                    tokenrow[11] = int(text["token"])
                if "Archer" in text["name"]:
                    tokenrow[12] = int(text["token"])
                if "Cholera" in text["name"]:
                    tokenrow[13] = int(text["token"])
                if "AnGarda" in text["name"]:
                    tokenrow[14] = int(text["token"])
                if "BealBocht" in text["name"]:
                    tokenrow[15] = int(text["token"])
                if "Cre" in text["name"]:
                    tokenrow[16] = int(text["token"])
                if "Narnia1" in text["name"]:
                    tokenrow[17] = int(text["token"])
                if "Run" in text["name"]:
                    tokenrow[18] = int(text["token"])
                if "Bulle" in text["name"]:
                    tokenrow[19] = int(text["token"])

            tokenwriter.writerow(tokenrow)
            #Get total number of tokens
            tottokens = sum(tokenrow[1:19])
            #Write sentence size
            sentencerow = [os.path.basename(lang),0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
            for text in texts:
                if "100" in text["name"]:
                    sentencerow[1] = text["sentence"]
                if "AAiW" in text["name"]:
                    sentencerow[2] = text["sentence"]
                if "Achter" in text["name"]:
                    sentencerow[3] = text["sentence"]
                if "mist" in text["name"]:
                    sentencerow[4] = text["sentence"]
                if "Rosa" in text["name"]:
                    sentencerow[5] = text["sentence"]
                if "Parfum" in text["name"]:
                    sentencerow[6] = text["sentence"]
                if "Prince" in text["name"]:
                    sentencerow[7] = text["sentence"]
                if "TtLG" in text["name"]:
                    sentencerow[8] = text["sentence"]
                if "Zahir" in text["name"]:
                    sentencerow[9] = text["sentence"]
                if "Zorba" in text["name"]:
                    sentencerow[10] = text["sentence"]
                if "AnimFarm" in text["name"]:
                    sentencerow[11] = int(text["sentence"])
                if "Archer" in text["name"]:
                    sentencerow[12] = int(text["sentence"])
                if "Cholera" in text["name"]:
                    sentencerow[13] = int(text["sentence"])
                if "AnGarda" in text["name"]:
                    sentencerow[14] = int(text["sentence"])
                if "BealBocht" in text["name"]:
                    sentencerow[15] = int(text["sentence"])
                if "Cre" in text["name"]:
                    sentencerow[16] = int(text["sentence"])
                if "Narnia1" in text["name"]:
                    sentencerow[17] = int(text["sentence"])
                if "Run" in text["name"]:
                    sentencerow[18] = int(text["sentence"])
                if "Bulle" in text["name"]:
                    sentencerow[19] = int(text["sentence"])

            sentencewriter.writerow(sentencerow)
            totsents = sum(sentencerow[1:19])
            #Get total number of nsubj
            nsubjrow = [os.path.basename(lang),0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
            for text in texts:
                if "100" in text["name"]:
                    nsubjrow[1] = text["nsubj"]
                if "AAiW" in text["name"]:
                    nsubjrow[2] = text["nsubj"]
                if "Achter" in text["name"]:
                    nsubjrow[3] = text["nsubj"]
                if "mist" in text["name"]:
                    nsubjrow[4] = text["nsubj"]
                if "Rosa" in text["name"]:
                    nsubjrow[5] = text["nsubj"]
                if "Parfum" in text["name"]:
                    nsubjrow[6] = text["nsubj"]
                if "Prince" in text["name"]:
                    nsubjrow[7] = text["nsubj"]
                if "TtLG" in text["name"]:
                    nsubjrow[8] = text["nsubj"]
                if "Zahir" in text["name"]:
                    nsubjrow[9] = text["nsubj"]
                if "Zorba" in text["name"]:
                    nsubjrow[10] = text["nsubj"]
                if "AnimFarm" in text["name"]:
                    nsubjrow[11] = int(text["nsubj"])
                if "Archer" in text["name"]:
                    nsubjrow[12] = int(text["nsubj"])
                if "Cholera" in text["name"]:
                    nsubjrow[13] = int(text["nsubj"])
                if "AnGarda" in text["name"]:
                    nsubjrow[14] = int(text["nsubj"])
                if "BealBocht" in text["name"]:
                    nsubjrow[15] = int(text["nsubj"])
                if "Cre" in text["name"]:
                    nsubjrow[16] = int(text["nsubj"])
                if "Narnia1" in text["name"]:
                    nsubjrow[17] = int(text["nsubj"])
                if "Run" in text["name"]:
                    nsubjrow[18] = int(text["nsubj"])
                if "Bulle" in text["name"]:
                    nsubjrow[19] = int(text["nsubj"])

            #nsubjwriter.writerow(nsubjrow)
            totnsubj = sum(nsubjrow[1:19])
            #Get total number of obj
            objrow = [os.path.basename(lang),0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
            for text in texts:
                if "100" in text["name"]:
                    objrow[1] = text["obj"]
                if "AAiW" in text["name"]:
                    objrow[2] = text["obj"]
                if "Achter" in text["name"]:
                    objrow[3] = text["obj"]
                if "mist" in text["name"]:
                    objrow[4] = text["obj"]
                if "Rosa" in text["name"]:
                    objrow[5] = text["obj"]
                if "Parfum" in text["name"]:
                    objrow[6] = text["obj"]
                if "Prince" in text["name"]:
                    objrow[7] = text["obj"]
                if "TtLG" in text["name"]:
                    objrow[8] = text["obj"]
                if "Zahir" in text["name"]:
                    objrow[9] = text["obj"]
                if "Zorba" in text["name"]:
                    objrow[10] = text["obj"]
                if "AnimFarm" in text["name"]:
                    objrow[11] = int(text["obj"])
                if "Archer" in text["name"]:
                    objrow[12] = int(text["obj"])
                if "Cholera" in text["name"]:
                    objrow[13] = int(text["obj"])
                if "AnGarda" in text["name"]:
                    objrow[14] = int(text["obj"])
                if "BealBocht" in text["name"]:
                    objrow[15] = int(text["obj"])
                if "Cre" in text["name"]:
                    objrow[16] = int(text["obj"])
                if "Narnia1" in text["name"]:
                    objrow[17] = int(text["obj"])
                if "Run" in text["name"]:
                    objrow[18] = int(text["obj"])
                if "Bulle" in text["name"]:
                    objrow[19] = int(text["obj"])

            #objwriter.writerow(objrow)
            totobj = sum(objrow[1:19])
            #Get total number of iobj
            iobjrow = [os.path.basename(lang),0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
            for text in texts:
                if "100" in text["name"]:
                    iobjrow[1] = text["iobj"]
                if "AAiW" in text["name"]:
                    iobjrow[2] = text["iobj"]
                if "Achter" in text["name"]:
                    iobjrow[3] = text["iobj"]
                if "mist" in text["name"]:
                    iobjrow[4] = text["iobj"]
                if "Rosa" in text["name"]:
                    iobjrow[5] = text["iobj"]
                if "Parfum" in text["name"]:
                    iobjrow[6] = text["iobj"]
                if "Prince" in text["name"]:
                    iobjrow[7] = text["iobj"]
                if "TtLG" in text["name"]:
                    iobjrow[8] = text["iobj"]
                if "Zahir" in text["name"]:
                    iobjrow[9] = text["iobj"]
                if "Zorba" in text["name"]:
                    iobjrow[10] = text["iobj"]
                if "AnimFarm" in text["name"]:
                    iobjrow[11] = int(text["iobj"])
                if "Archer" in text["name"]:
                    iobjrow[12] = int(text["iobj"])
                if "Cholera" in text["name"]:
                    iobjrow[13] = int(text["iobj"])
                if "AnGarda" in text["name"]:
                    iobjrow[14] = int(text["iobj"])
                if "BealBocht" in text["name"]:
                    iobjrow[15] = int(text["iobj"])
                if "Cre" in text["name"]:
                    iobjrow[16] = int(text["iobj"])
                if "Narnia1" in text["name"]:
                    iobjrow[17] = int(text["iobj"])
                if "Run" in text["name"]:
                    iobjrow[18] = int(text["iobj"])
                if "Bulle" in text["name"]:
                    iobjrow[19] = int(text["iobj"])

            #iobjwriter.writerow(iobjrow)
            totiobj = sum(iobjrow[1:19])
        #Write total stats
        statswriter.writerow([os.path.basename(lang), tottokens, totsents,totnsubj,totobj,totiobj])
        print("Done with "+lang)
    print("--- %s seconds ---" % (time.time() - start_time))
    print("Done! Happy corpus-based typological linguistics!\n")

if __name__ == "__main__":
    main()
    sys.exit(0)

