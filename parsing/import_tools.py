#!/usr/bin/env python3
import sys
import subprocess
import re
import glob
from pathlib import Path
from tqdm import tqdm
import os
import csv
from io import StringIO



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

import unicodedata, re
import xml.etree.cElementTree as ET

def importRSC(file_content):
    file_content = re.sub(r'<page.*?>|</page.*?>|<normalised.*?>|</normalised.*?>', '', file_content)
    #Remove empy lines
    file_content = os.linesep.join([s for s in file_content.splitlines() if s])   
    vrt = ET.fromstring(file_content)
    metadata = vrt.attrib
    #Child must be <s>...</s>
    rsc = []
    for v in vrt:
        vrtclean = StringIO(v.text)
        sentence = []
        for t in vrtclean:
            if t and t != "\n":
                sentence.append(t.split('\t')[0])
        rsc.append(sentence)
    return rsc,metadata

