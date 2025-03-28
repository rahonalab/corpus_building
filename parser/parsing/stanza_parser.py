from stanza.utils.conll import CoNLL
from parsing.clean_text import preparetext
import os
import json
from pathlib import Path

from parsing.import_tools import sentPysbd

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

#This function prepares the NLP pipeline
def preparenlpconf(model, pipeline):
    #Build a simple config
    config= {'lang':model,'processors':pipeline}
    if model == "sq": 
            modelpath = input("Path to model: ")
            tokenize = input("Tokenize model: ")
            mwt = input("Mwt model: ")
            pos = input("Pos model: ")
            lemma = input("Lemma model: ")
            depparse = input("Depparse model: ")
            pretrain = input("Pretrain: ")
            config.update({
                        # Language code for the language to build the Pipeline in
                        # Processor-specific arguments are set with keys "{processor_name}_{argument_name}"
                        # You only need model paths if you have a specific model outside of stanza_resources
	                    'tokenize_model_path': modelpath+"/tokenize/"+tokenize,
                        'mwt_model_path' : modelpath+"/mwt/"+mwt,
	                    'pos_model_path': modelpath+"/pos/"+pos,
	                    'lemma_model_path': modelpath+"/lemma/"+lemma,
	                    'depparse_model_path': modelpath+"/depparse/"+depparse,
                        'pos_pretrain_path': modelpath+"/pretrain/"+pretrain,
                        'depparse_pretrain_path': modelpath+"/pretrain/"+pretrain,
                        })
    return config

def load_config(infile: Path):
    with open(infile, encoding="utf-8") as fin:
        config = json.load(fin)
    return config


#Distinguish between CIEP+ and miniciep+

def parseminiciep(nlp,text,filename,target):
    print("Parsing "+filename)
    # Create mini/ folder if it does not exit
    if not os.path.exists(target + "/" + "mini" + "/"):
        os.makedirs(target + "/" + "mini" + "/")
    if not os.path.exists(target + "/" + "mid" + "/"):
        os.makedirs(target + "/" + "mid" + "/")
    if '===endminiciep+===' in text:
        print("endminiciep+ string found")
        '''Split between CIEP+, miniCIEP+ and midCIEP+'''
        splitciep = text.split('===endminiciep+===')
        miniciepf = target + "/" + "mini" + "/" + Path(filename).stem + ".conllu"
        midciepf = target + "/" + "mid" + "/" + Path(filename).stem + ".conllu"
        print("Parsing miniciep+")
        miniciept = nlp(preparetext(splitciep[0]))
        CoNLL.write_doc2conll(miniciept, miniciepf)

def parseciep(nlp,text,filename,target):
    print("Parsing "+filename)
    if not os.path.exists(target+"/"+"full"+"/"):
        os.makedirs(target+"/"+"full"+"/")
    ciepf = target+"/full/"+Path(filename).stem+".conllu"
    print('Parsing full CIEP+')
    ciep = nlp(preparetext(text))
    CoNLL.write_doc2conll(ciep,ciepf)

def parsealtminiciep(nlp,text,filename,target,lang):
    print("Parsing "+filename)
    # Create mini/ folder if it does not exit
    if not os.path.exists(target + "/" + "mini" + "/"):
        os.makedirs(target + "/" + "mini" + "/")
    if not os.path.exists(target + "/" + "mid" + "/"):
        os.makedirs(target + "/" + "mid" + "/")
    if '===endminiciep+===' in text:
        print("endminiciep+ string found")
        '''Split between CIEP+, miniCIEP+ and midCIEP+'''
        splitciep = text.split('===endminiciep+===')
        miniciepf = target + "/" + "mini" + "/" + Path(filename).stem + ".conllu"
        midciepf = target + "/" + "mid" + "/" + Path(filename).stem + ".conllu"
        miniciept = preparetext(splitciep[0])
        miniciept = sentPysbd(lang, miniciept)
        print("Parsing miniciep+, using pysbd")
        miniciepconll = nlp(miniciept)
        CoNLL.write_doc2conll(miniciepconll, miniciepf)


def parsealtciep(nlp,text,filename,target,lang):
    print("Parsing " + filename)
    if not os.path.exists(target + "/" + "full" + "/"):
       os.makedirs(target + "/" + "full" + "/")
    ciepf = target+"/full/"+Path(filename).stem+".conllu"
    ciep = preparetext(text)
    print('Parsing full CIEP+, using pysbd')
    ciep = sentPysbd(lang, ciep)
    ciepconll = nlp(ciep)
    CoNLL.write_doc2conll(ciepconll,ciepf)

#...while this other function is generic:
def parseother(nlp,text,filename,target):
    conllu = target+Path(filename).stem+".conllu"
    other = nlp(preparetext(text))
    CoNLL.write_doc2conll(other,conllu)

#...while this one is for already-prepared text
def parseprepared(nlp,text,filename,target):
    conllu = target+Path(filename).stem+".conllu"
    prepared = nlp(text)
    CoNLL.write_doc2conll(prepared,conllu)
