# """ from https://github.com/keithito/tacotron """

# """
# Defines the set of symbols used in text input to the model.

# The default is a set of ASCII characters that works well for English or text that has been run through Unidecode. For other data, you can modify _characters. See TRAINING_DATA.md for details. """

# from text import cmudict, tagdict

# _pad = "_"
# _punctuation = "!'(),.:;? "
# _special = "-/"
# _letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
# _silences = ["@sp", "@spn", "@sil"]

# # Prepend "@" to ARPAbet symbols to ensure uniqueness (some are the same as uppercase letters):
# _arpabet = ["@" + s for s in cmudict.valid_symbols]
# #_pinyin = ["@" + s for s in pinyin.valid_symbols]
# _tagdict = ["@" + s for s in tagdict.valid_symbols]

# # Export all symbols:
# symbols = (
#     [_pad]
#     + list(_special)
#     + list(_punctuation)
#     + list(_letters)
#     + _arpabet
#     #+ _tagdict
#     #+ _pinyin
#     + _silences
# )

"""Dynamic symbol loading system - Self-initializing Version"""

from config import preprocess_config
from pathlib import Path

_symbols = None
_symbol_to_id = None
_id_to_symbol = None
_symbols_file = None
_initialized = False

def load_symbols(symbols_file):
    """Load symbols from file, normalizing space symbols to single space"""
    symbols = []
    with open(symbols_file, 'r', encoding='utf-8') as f:
        for line in f:
            stripped = line.strip()
            if not stripped:  # Skip empty lines
                continue
            
            # Find first token (symbol)
            parts = line.split(maxsplit=1)
            if not parts:
                continue
                
            symbol = parts[0]
            
            # Special case: if line starts with space(s) before number
            if line[0] == ' ' and line[1] == ' ' and symbol.isdigit():
                symbol = ''  # Normalize to empty (as needed by efficientspeech, all spaces are removed)
            
            symbols.append(symbol)
    return symbols


def initialize_symbols():
    """Initialize the symbol system"""
    global _symbols, _symbol_to_id, _id_to_symbol, _initialized
    if not _initialized:
        symbols_file = Path(preprocess_config["path"]["tokens_path"])
        _symbols = load_symbols(symbols_file)
        _symbol_to_id = {s: i for i, s in enumerate(_symbols)}
        _id_to_symbol = {i: s for i, s in enumerate(_symbols)}
        _initialized = True

def get_symbols():
    """Get symbols, initializing if needed"""
    initialize_symbols()
    return _symbols

def get_symbol_to_id():
    """Get symbol to ID mapping, initializing if needed"""
    initialize_symbols()
    return _symbol_to_id

def get_id_to_symbol():
    """Get ID to symbol mapping, initializing if needed"""
    initialize_symbols()
    return _id_to_symbol

# Backward compatibility
symbols = property(get_symbols)