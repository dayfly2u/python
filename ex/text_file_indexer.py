"""
text_file_indexer.py
a program to index a text file
author: ...
copyright 2016 ...
"""

import sys
import os
import string

def index_text_file(txt_filename, idx_filename,
                    delimiter_chars = ",.;:!?") :
    try:
        txt_fil = open(txt_filename, "r")

        word_occurrences = {}
        line_num = 0

        for lin in txt_fil:
            line_num += 1
            # split line into words delimited by whitespace
            words = lin.split()
            
