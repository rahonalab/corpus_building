#!/usr/bin/env python3
import sys
import subprocess
import re
import glob
from pathlib import Path
from tqdm import tqdm
import os,sys
from html.parser import HTMLParser
import unicodedata, re


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

USAGE = './readfromxml-D.py -f file -m path_to_metadata'

def build_parser():

    parser = argparse.ArgumentParser(description='clean raw txt and extract metadata')
    parser.add_argument('-f', dest="filename", required=True, help='file')
    parser.add_argument('-m', dest="metadata", required=True, help='path_to_metadata')    
    
    return parser

class metaParser(HTMLParser):
    data_tags = ["text","p","page"]
    capture_meta = False
    meta_data = {}
    key = ""
    def handle_starttag(self, tag, attrs):
        if tag not in self.data_tags:
            self.capture_meta = True
            self.key = tag

    def handle_endtag(self, tag):
        if tag not in self.data_tags:
            self.capture_meta = False

    def handle_data(self, data):
        if self.capture_meta:
            self.meta_data[self.key] = data
    
    def get_meta_data(self):
        return self.meta_data


class textParser(HTMLParser):

    def __init__(self):
        super().__init__()
        self.data = []
        self.capture = False

    def handle_starttag(self, tag, attrs):
        if tag in ('text'):
            self.capture = True

    def handle_endtag(self, tag):
        if tag in ('text'):
            self.capture = False

    def handle_data(self, data):
        if self.capture:
            self.data.append(data)

all_chars = (unichr(i) for i in range(0x110000))
control_chars = ''.join(map(chr, list(range(0,32)) + list(range(127,160))))

control_char_re = re.compile('[%s]' % re.escape(control_chars))

def sanitize(s):
    return unicodedata.normalize('NFC', control_char_re.sub(' ', s))

def sentencesplit(file_content):
    file_content = os.linesep.join([s for s in file_content.splitlines() if s])   
    parser = metaParser()
    parser.feed(file_content)
    #Write metadata
    metadata= open(args.metadata+Path(args.filename).stem+".metadata","w+")
    metadata.write("<text ")
    doc_meta_data = parser.get_meta_data()
    for i,m in enumerate(doc_meta_data):
        metadata.write(m + "=\"" + doc_meta_data[m] + "\"")
        if i != len(doc_meta_data) - 1:
            metadata.write(" ")
    metadata.write(">")
    #Print out text
    parser = textParser()
    parser.feed(file_content)
    for s in parser.data:
        print(s)


def main():
    global debug
    parser = build_parser()
    global args
    args = parser.parse_args()
    '''Check arguments'''    
    if check_args(args) is False:
     sys.stderr.write("There was a problem validating the arguments supplied. Please check your input and try again. Exiting...\n")
     sys.exit(1)

    '''Unknown function, I'll check it later''' 
    start_time = time.time()
    file_content = open(args.filename).read()
    sentencesplit(file_content)

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

