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

all_chars = (unichr(i) for i in range(0x110000))
control_chars = ''.join(map(chr, list(range(0,32)) + list(range(127,160))))

control_char_re = re.compile('[%s]' % re.escape(control_chars))

def sanitize(s):
    return unicodedata.normalize('NFC', control_char_re.sub(' ', s))


def preparetext(file_content):
    '''Clean up nasty characters'''
    #output=sanitize(re.sub(r'(?m)^\@.*\n?',' ',file_content.replace('’', '\'').replace('‘', '\'')).replace('…',' ... ').replace('«',' " ').replace('»',' " ').replace('<BLOCK>',' ').replace('“',' " ').replace('”',' " ').replace('„',' " ').replace('* * *',' . ').replace('‚','\'').replace('','').replace('‬','').replace('‌','').replace('===endminiciep+===','').replace('\ufeff', ''))
    output=sanitize(re.sub(r'(?m)^\@.*\n?',' ',file_content.replace('’', '\'').replace('‘', '\'')).replace('…','...').replace('<BLOCK>',' ').replace('“','"').replace('”','"').replace('„','"').replace('* * *',' . ').replace('‚','\'').replace('‬','').replace('‌','').replace('===endminiciep+===','').replace('\ufeff', ''))
    output=re.sub(r'[ \t]{2,}', ' ', output)
    return output

