import argparse
import glob
import sys
from contextlib import redirect_stdout
from os.path import basename
from pathlib import Path

from bertalign import Bertalign

USAGE = './sentence-aligner --lang1 --lang2 '

def build_parser():

    parser = argparse.ArgumentParser(description='sentence-aligner for CIEP+')

    parser.add_argument('--lang1', required=True, help='Lang1 texts')
    parser.add_argument('--lang2', required=True, help='Lang2 texts')
    parser.add_argument( '--target', required=True, help='Target destination for sentence-split file')
    return parser

def check_args(args):
    '''Exit if required arguments not specified'''
    check_flags = {}

def main():
    global args
    parser = build_parser()
    args = parser.parse_args()
    target = args.target
    for filename1 in sorted(glob.glob(args.lang1+'/*.txt')):
        filelang1 = open(filename1, encoding='utf-8').read()
        print("Reading: " + filename1)
        for filename2 in sorted(glob.glob(args.lang2+'/*.txt')):
            if Path(filename1).stem.split("_")[0] == Path(filename2).stem.split("_")[0]:
                lang1 = Path(filename1).stem.split("_")[1]
                lang2 = Path(filename2).stem.split("_")[1]
                book = Path(filename1).stem.split("_")[0]
                filelang2 = open(filename2, encoding='utf-8').read()
                print("It's a match! Starting the alignment of "+Path(filename1).stem+" with "+Path(filename2).stem)
                sentsplitfile = book+"_"+lang1+"-"+lang2
                aligner = Bertalign(filelang1, filelang2)
                aligner.align_sents()
                with open(target+sentsplitfile, 'w') as f:
                    with redirect_stdout(f):
                        aligner.print_sents()

if __name__ == "__main__":
    main()
    sys.exit(0)