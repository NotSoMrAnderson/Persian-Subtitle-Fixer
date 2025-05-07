from io import open
from os import path
from time import sleep
from chardet import detect
import re


def is_persian_arabic_text(text):
    """Check if the text contains Persian/Arabic characters."""
    # Unicode ranges for Persian and Arabic
    persian_arabic_pattern = re.compile(r'[\u0600-\u06FF\u0750-\u077F\uFB50-\uFDFF\uFE70-\uFEFF]+')
    
    # Check if there's a significant amount of Persian/Arabic text
    matches = persian_arabic_pattern.findall(text)
    if not matches:
        return False
    
    # Calculate the ratio of Persian/Arabic characters
    total_text_length = len(''.join(text.split()))  # Remove whitespace
    persian_arabic_length = sum(len(match) for match in matches)
    
    # Return True if at least 20% of the text is Persian/Arabic
    return (persian_arabic_length / total_text_length) > 0.2


def detect_encoding(file_path):
    """Detect the encoding of a file using chardet."""
    with open(file_path, 'rb') as file:
        raw_data = file.read()
    return detect(raw_data)['encoding']


def try_encodings(file_path):
    """Try multiple encodings and return content with successful encoding."""
    # Prioritized encodings for Persian/Arabic subtitle files
    encodings = [
        'cp1256',      # Windows Arabic
        'windows-1256',# Windows Arabic (alternative name)
        'utf-8',       # Unicode
        'utf-8-sig',   # Unicode with BOM
        'arabic',      # ISO-8859-6
        'iso-8859-6',  # Arabic alphabet
        'mac-farsi'    # MacOS Farsi
    ]
    
    # First try detected encoding
    detected = detect_encoding(file_path)
    if detected:
        encodings.insert(0, detected)
    
    errors = {}
    for encoding in encodings:
        try:
            with open(file_path, mode="r", encoding=encoding) as fd:
                content = fd.read()
                # Only process if it contains Persian/Arabic text
                if is_persian_arabic_text(content):
                    return content, encoding
                else:
                    errors[encoding] = "No Persian/Arabic text detected"
        except UnicodeDecodeError as e:
            errors[encoding] = str(e)
            continue
    
    raise ValueError("Either the file is not a Persian/Arabic subtitle or it's corrupted. Tried encodings: " + str(errors))


def fixer(Fpath, Form):
    try:
        content, used_encoding = try_encodings(Fpath)
        
        if Fpath.find(Form, -1):
            new_path = Fpath[:-4] + f'.edited{Form}'
            
            with open(new_path, mode="w", encoding="utf-8") as fd:
                fd.write(content)
            
            return True, f"Successfully converted Persian/Arabic subtitle from {used_encoding} to UTF-8"
    except Exception as e:
        return False, f"Error processing file: {str(e)}"


def Fcheck(Fpath):
    if path.isdir(Fpath):
        # print("\nIt is a directory")
        return False
    elif path.isfile(Fpath):
        # print("\nIt is a normal file")
        return True
    else:
        # print("It is a special file (socket, FIFO, device file)")
        return False


def useless(Dfile):
    for form in ['.srt', '.ass', '.SRT']:
        if Dfile.endswith(form):
            return form


def main(Flist):
    count = 0

    total = len(Flist)
    for items in Flist:
        if Fcheck(items):
            try:
                with open(items, mode="r", encoding="utf-8") as fd:
                    fd.read()
            except UnicodeDecodeError:
                count += 1
                fixer(items, useless(items))
                sleep(0.2)
    return total - count
