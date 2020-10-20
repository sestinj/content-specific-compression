import os
from zipfile import ZipFile
import re
import nltk

ROOT_DIR = '/Users/natesesti/Desktop/mtc'

def convert_to_bits(string):
    """Create and return an array of bits for each character of a string"""

    bytes = bytearray(string, 'utf-8')
    bitarray = list(map(bin, bytes))
    return bitarray

def create_conversion(n=8, path=ROOT_DIR + '/masc_500k_texts'):
    """Create a dictionary of size 2^n (default can be represented by a single byte)
    that maps most common tokens to binary.
    Uses the masc_500k_texts corpus by default"""

    common = most_common(tokenize_directory(path), 2**n)
    conversion = {}
    for i in range(len(common)):
        conversion[common[i][0]] = bin(i).split('0b')[1]
    return conversion

def most_common(tokens, n=50):
    return nltk.FreqDist(tokens).most_common(n)

def tokenize_file(path):
    """Given a path to a txt file, return word tokenization of that file."""
    text = open(path, encoding='iso-8859-15').read()
    return nltk.word_tokenize(text)

def tokenize_directory(path=os.getcwd()):
    """Given a path to a directory, recursively traverse to
    add all .txt files to the token list."""

    tokens = []

    os.chdir(path)

    subpaths = os.listdir()

    for subpath in subpaths:
        if subpath.endswith('.txt'):
            tokens += tokenize_file(subpath)
        elif os.path.isdir(subpath):
            tokens += tokenize_directory(subpath)

    return tokens

def compress(path, conversion):
    """Given path to a file,
    create a new compressed .txt file, named path+_compressed.txt.
    Return the path to the new file."""
    os.chdir(ROOT_DIR)
    write_file = open(path.split('.')[0] + '_compressed.txt', 'wb')

    for token in tokenize_file(path):
        if token in conversion:
            write_file.write(conversion[token])
        else:
            for bits in convert_to_bits(token):
                write_file.write(bits)

    return path

def compare_sizes(path):
    """Given path to a file,
    compress it and compare the original size to compressed.
    Returns percent compression as a decimal."""

    original_size = os.path.getsize(path) #Size in bytes

    compressed_size = os.path.getsize(compress(path))

    return (original_size - compressed_size) / original_size

def zip_compare(path):
    """Given path to a file,
    compare size of zipped file and compressed then zipped file."""

    zipped_original = ZipFile(path.split('.')[0] + '.zip', 'w').write(path)

    compressed = compress(path)

    zipped_compressed = ZipFile(compressed.split('.')[0] + '.zip', 'w').write(compressed)

    original_size = os.path.getsize(zipped_original)

    compressed_size = os.path.getsize(zipped_compressed)

    return (original_size - compressed_size)/original_size