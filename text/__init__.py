"""Text processing module with safe initialization"""
import re
from . import cleaners
from .symbols import get_symbols, get_symbol_to_id, get_id_to_symbol

def text_to_sequence(text, cleaner_names):
    """Convert text to phoneme IDs"""
    sequence = []
    while len(text):
        m = _curly_re.match(text)
        if not m:
            sequence += _symbols_to_sequence(_clean_text(text, cleaner_names))
            break
        sequence += _symbols_to_sequence(_clean_text(m.group(1), cleaner_names))
        sequence += _arpabet_to_sequence(m.group(2))
        text = m.group(3)
    return sequence

def sequence_to_text(sequence):
    """Convert phoneme IDs to text"""
    _id_to_symbol = get_id_to_symbol()
    result = ""
    for symbol_id in sequence:
        if symbol_id in _id_to_symbol:
            s = _id_to_symbol[symbol_id]
            if len(s) > 1 and s[0] == "@":
                s = "{%s}" % s[1:]
            result += s
    return result.replace("}{", " ")

# Rest of the original functions remain unchanged
def _clean_text(text, cleaner_names):
    for name in cleaner_names:
        cleaner = getattr(cleaners, name)
        if not cleaner:
            raise Exception("Unknown cleaner: %s" % name)
        text = cleaner(text)
    return text

def _symbols_to_sequence(symbols):
    _symbol_to_id = get_symbol_to_id()
    return [_symbol_to_id[s] for s in symbols if _should_keep_symbol(s)]

def _arpabet_to_sequence(text):
    return _symbols_to_sequence(["@" + s for s in text.split()])

def _should_keep_symbol(s):
    _symbol_to_id = get_symbol_to_id()
    return s in _symbol_to_id and s != "_" and s != "~"

# Regular expression matching text enclosed in curly braces:
_curly_re = re.compile(r"(.*?)\{(.+?)\}(.*)")

# Backward compatibility
symbols = property(get_symbols)