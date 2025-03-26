"""Basic text cleaners for IPA symbols"""

import re

_whitespace_re = re.compile(r'\s+')

def basic_cleaners(text):
    '''Basic pipeline that normalizes whitespace'''
    text = re.sub(_whitespace_re, ' ', text).strip()
    return text