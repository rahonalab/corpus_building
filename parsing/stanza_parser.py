from pathlib import Path
import stanza
from stanza.utils.conll import CoNLL
from parsing.clean_text import preparetext
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
def preparenlp(model,processors,corpus):
    if model == "test": 
            modelpath = input("Path to model: ")
            tokenize = input("Tokenize model: ")
            mwt = input("Mwt model: ")
            pos = input("Pos model: ")
            lemma = input("Lemma model: ")
            depparse = input("Depparse model: ")
            pretrain = input("Pretrain: ")
            config = {
                        # Comma-separated list of processors to use
	                    'processors': 'tokenize,pos,lemma,depparse',
                        # Language code for the language to build the Pipeline in
                        'lang': 'fr',
                        # Processor-specific arguments are set with keys "{processor_name}_{argument_name}"
                        # You only need model paths if you have a specific model outside of stanza_resources
	                    'tokenize_model_path': modelpath+"/tokenize/"+tokenize,
	                    'pos_model_path': modelpath+"/pos/"+pos,
	                    'lemma_model_path': modelpath+"/lemma/"+lemma,
	                    'depparse_model_path': modelpath+"/depparse/"+depparse,
                        'pos_pretrain_path': modelpath+"/pretrain/"+pretrain,
                        'depparse_pretrain_path': modelpath+"/pretrain/"+pretrain,
                        }
            nlp = stanza.Pipeline(**config,logging_level="DEBUG") # Initialize the pipeline using a configuration dict
    else:
            nlp = stanza.Pipeline(lang=model, logging_level="DEBUG", processors=processors)         
    return nlp


#This functions is dedicated to the parsing of CIEP+...
def parseciep(nlp,text,filename,target,miniciep):
    ciepf = target+"/"+Path(filename).stem+".conllu"
    '''Select the type of output: Both (yes), only ciep (no), only miniciep (only)'''
    if miniciep == "yes" or "only":
            if '===endminiciep+===' in text:
                print("endminiciep+ string found")
                '''Split between CIEP+ and miniCIEP+'''
                splitciep = text.split('===endminiciep+===')
                miniciepf = target+"/"+"mini"+"/"+Path(filename).stem+".conllu"
                print("Parsing miniciep+")
                miniciep = nlp(preparetext(splitciep[0]))
                CoNLL.write_doc2conll(miniciep,miniciepf)
            if miniciep == "yes":
                ciepf = target+"/"+Path(filename).stem+".conllu"
                print("Parsing full ciep+")
                ciep = nlp(preparetext(text))
                CoNLL.write_doc2conll(ciep,ciepf)
    if miniciep == "no": 
            print('Parsing only CIEP+')
            ciepf = target+"/"+Path(filename).stem+".conllu"
            ciep = nlp(preparetext(text))
            CoNLL.write_doc2conll(ciep,ciepf)


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
