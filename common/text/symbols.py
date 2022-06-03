""" from https://github.com/keithito/tacotron """

'''
Defines the set of symbols used in text input to the model.

The default is a set of ASCII characters that works well for English or text that has been run through Unidecode. For other data, you can modify _characters. See TRAINING_DATA.md for details. '''
from .cmudict import valid_symbols


# Prepend "@" to ARPAbet symbols to ensure uniqueness (some are the same as uppercase letters):
_arpabet = ['@' + s for s in valid_symbols]


def get_symbols(symbol_set='russian_basic'):
    if symbol_set == 'russian_basic':
        _pad = '_'
        _punctuation = '+!\'(),.:;? '
        _special = '-'
        _letters = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдеёжзийклмнопрстуфхцчшщъыьэюя'
        symbols = list(_pad + _special + _punctuation + _letters) + _arpabet
    elif symbol_set == 'russian_basic_lowercase':
        _pad = '_'
        _punctuation = '+!\'"(),.:;? '
        _special = '-'
        _letters = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
        symbols = list(_pad + _special + _punctuation + _letters) + _arpabet
    else:
        raise Exception("{} symbol set does not exist".format(symbol_set))

    return symbols


def get_pad_idx(symbol_set='russian_basic'):
    if symbol_set in {'russian_basic', 'russian_basic_lowercase'}:
        return 0
    else:
        raise Exception("{} symbol set not used yet".format(symbol_set))
