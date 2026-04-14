import unicodedata, re

# FIX: We create the list of control characters but EXCLUDE 10 (\n) and 13 (\r)
# range(0, 32) includes 0 through 31. We skip 10 and 13.
control_indices = [i for i in range(0, 32) if i not in (10, 13)] + list(range(127, 160))
control_chars = ''.join(map(chr, control_indices))

control_char_re = re.compile('[%s]' % re.escape(control_chars))


def sanitize(s):
    # This now removes "invisible" junk but keeps your newlines intact
    return unicodedata.normalize('NFC', control_char_re.sub(' ', s))


def preparetext(file_content):
    '''Clean up nasty characters while preserving structure'''
    # 1. Handle the @ lines (removes lines starting with @)
    output = re.sub(r'(?m)^\@.*\n?', '', file_content)

    # 2. Replace curly quotes and special punctuation
    replacements = {
        '’': "'", '‘': "'", '‚': "'",
        '“': '"', '”': '"', '„': '"',
        '«': '"', '»': '"',
        '…': '...', '* * *': ' . ',
        '—': '-', '–': '-'
    }
    for old, new in replacements.items():
        output = output.replace(old, new)

    # 3. Remove specific hidden markers
    output = output.replace('‬', '').replace('‌', '').replace('===endminiciep+===', '').replace('\ufeff', '')

    # 4. Sanitize (removes non-newline control chars)
    output = sanitize(output)

    # 5. Collapse multiple horizontal spaces/tabs into one, but leave newlines alone
    output = re.sub(r'[ \t]{2,}', ' ', output)

    return output


def doublespacing(file_content):
    # Standardizes to double newlines
    return "\n\n".join(file_content.splitlines())