#!/usr/bin/env python3
import sys
import re
import glob
from pathlib import Path
import os
import argparse

from parsing.clean_text import preparetext

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

USAGE = './make-miniciep+.py -s <source_directory> -t <target_directory> [-h] '

def build_parser():

    parser = argparse.ArgumentParser(description='make-miniciep+ - generate miniciep+, the sharable version of the wonderful CIEP+')


    parser.add_argument('-s', '--source', required=True, help='Source for raw texts, must be dir/dir/dir')
    parser.add_argument('-t', '--target', required=True, help='Target destination for processed texts')

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
    target = args.target
    '''Check arguments'''    
    if check_args(args) is False:
     sys.stderr.write("There was a problem validating the arguments supplied. Please check your input and try again. Exiting...\n")
     sys.exit(1)
    '''Unknown function, I'll check it later''' 
    start_time = time.time()

    for filename in sorted(glob.glob(args.source+'/*.txt')):
        file_content = open(filename, encoding='utf-8').read()
        lang = Path(filename).stem.split("_")[1]
        print("Reading: " + filename)
        if '===endminiciep+===' in file_content:
            print("endminiciep+ string found")
            '''Extract metadata'''
            # Create metatada folder if it does not exist
            if not os.path.exists(target + lang + "/metadata"):
                os.makedirs(target + lang + "/metadata")
            #Handle BOM
            header = re.findall(r'@.*', file_content.replace('\ufeff', ''))
            try:
                header.remove('@endheader')
            except:
                pass
            metadata = open(target + lang + "/metadata/" + Path(filename).stem + ".metadata", "w+")
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
            print("Splitting " + filename)
            # Create lang/ folder if it does not exist
            if not os.path.exists(target + lang):
                os.makedirs(target + lang)

            # Create mini/ folder if it does not exit
            if not os.path.exists(target + lang + "/" + "mini" + "/"):
                os.makedirs(target + lang + "/" + "mini" + "/")
            '''Split miniciep+'''
            splitciep = file_content.split('===endminiciep+===')
            with open(target + lang + "/" + "mini" + "/" + Path(filename).stem + ".txt", "w", encoding="utf-8") as f:
                f.write(preparetext(splitciep[0]))
    print("--- %s seconds ---" % (time.time() - start_time))
    print("Done! Happy corpus-based typological linguistics!\n")

if __name__ == "__main__":
    main()
    sys.exit(0)

