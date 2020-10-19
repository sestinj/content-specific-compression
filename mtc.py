import os
from zipfile import ZipFile
import re
import nltk



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

def create_map(tokens):
    pass

def compress(path, map):
    """Given path to a file,
    create a new compressed .txt file, named path+_compressed.txt.
    Return the path to the new file."""

    file = open(path.split('.')[0] + '_compressed.txt', 'w')
    file.write()

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