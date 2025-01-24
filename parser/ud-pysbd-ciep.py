from parsing.clean_text import preparetext
from parsing.import_tools import sentPysbd
from pathlib import Path
import glob
import argparse
import re
import os
import sys
USAGE = './ud-stanza-ciep.py -s <source_directory> -t <target_directory> -l <language> -m <metadata_directory> -p <alternative sentence splitter> [-h] '

def build_parser():

    parser = argparse.ArgumentParser(description='ud-pysbd - sentence splitting with pySBD')

    parser.add_argument('-s', '--source', required=True, help='Source for raw texts, must be dir/dir/dir')
    parser.add_argument('-t', '--target', required=True, help='Target destination for processed texts')
    parser.add_argument('-m', '--metadata', required=True, help='Target destination for metadata')
    parser.add_argument('-l', '--model', required=True, help='Language model e.g., en for English, zh for Chinese. Use mine for custom models.')
    parser.add_argument('-c', '--miniciep', required=False, help='Create miniciep+')


    return parser

def check_args(args):
    '''Exit if required arguments not specified'''
    check_flags = {}

def main():
    global args
    parser = build_parser()
    args = parser.parse_args()
    target = args.target
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
        if args.miniciep == "yes":
            # Create mini/ folder if it does not exit
            if not os.path.exists(target + "/" + "mini" + "/"):
                os.makedirs(target + "/" + "mini" + "/")
            if not os.path.exists(target + "/" + "mid" + "/"):
                os.makedirs(target + "/" + "mid" + "/")
            if '===endminiciep+===' in file_content:
                print("endminiciep+ string found")
                '''Split between CIEP+, miniCIEP+ and midCIEP+'''
                splitciep = file_content.split('===endminiciep+===')
                miniciepf = open(args.target + "/" + "mini" + "/" + Path(filename).stem + ".txt","w+")
                print("Sentence-splitting miniciep+")
                miniciep = preparetext(splitciep[0])
                miniciep = sentPysbd(args.model, miniciep)
                miniciepf.write(miniciep)
                miniciepf.close()
        else:
            print('Sentence-splitting full CIEP+')
            if not os.path.exists(target + "/" + "full" + "/"):
                os.makedirs(target + "/" + "full" + "/")
            ciepf = open(args.target + "/" + "full" + "/" + Path(filename).stem + ".txt", "w+")
            ciep = preparetext(file_content)
            ciep = sentPysbd(args.model, ciep)
            ciepf.write(ciep)
            ciepf.close()
if __name__ == "__main__":
    main()
    sys.exit(0)