import re
_letters_and_numbers_re = re.compile(
    r"((?:[а-яА-Я]+[0-9]|[0-9]+[а-яА-Я])[а-яА-Я0-9']*)", re.IGNORECASE)

_hardware_re = re.compile(
    '([0-9]+(?:[.,][0-9]+)?)(?:\s?)(тб|гб|мб|кб|гц|мм|см|м|км)', re.IGNORECASE)
_hardware_key = {'тб': 'терабайт',
                 'гб': 'гигабайт',
                 'мб': 'мегабайт',
                 'кб': 'килобайт',
                 'гц': 'герц',
                 'мм': 'милиметров',
                 'см': 'сантиметров',
                 'м': 'метров',
                 'км': 'километров'}

_dimension_re = re.compile(
    r'\b(\d+(?:[,.]\d+)?\s*[xXхХ]\s*\d+(?:[,.]\d+)?\s*[xXхХ]\s*\d+(?:[,.]\d+)?(?:мм|см|м)?)\b|\b(\d+(?:[,.]\d+)?\s*[xXхХ]\s*\d+(?:[,.]\d+)?(?:мм|см|м)?)\b')
_dimension_key = {'м': 'метр',
                  'см': 'сантиметр',
                  'мм': 'милиметр'}




def _expand_letters_and_numbers(m):
    text = re.split(r'(\d+)', m.group(0))

    # remove trailing space
    if text[-1] == '':
        text = text[:-1]
    elif text[0] == '':
        text = text[1:]

    # if not like 1920s, or AK47's , 20th, 1st, 2nd, 3rd, etc...
    if text[-1] in ("'ой", "ий", "ый", "ого", "его", "ым") and text[-2].isdigit():
        text[-2] = text[-2] + text[-1]
        text = text[:-1]

    # for combining digits 2 by 2
    new_text = []
    for i in range(len(text)):
        string = text[i]
        if string.isdigit() and len(string) < 5:
            # heuristics
            if len(string) > 2 and string[-2] == '0':
                if string[-1] == '0':
                    string = [string]
                else:
                    string = [string[:-2], string[-2], string[-1]]
            elif len(string) % 2 == 0:
                string = [string[i:i+2] for i in range(0, len(string), 2)]
            elif len(string) > 2:
                string = [string[0]] + [string[i:i+2] for i in range(1, len(string), 2)]
            new_text.extend(string)
        else:
            new_text.append(string)

    text = new_text
    text = " ".join(text)
    return text


def _expand_hardware(m):
    quantity, measure = m.groups(0)
    measure = _hardware_key[measure.lower()]
    if measure[-1] != 'z' and float(quantity.replace(',', '')) > 1:
        return "{} {}s".format(quantity, measure)
    return "{} {}".format(quantity, measure)


def _expand_dimension(m):
    text = "".join([x for x in m.groups(0) if x != 0])
    text = text.replace(' x ', ' на ')
    text = text.replace('x', ' на ')
    if text.endswith(tuple(_dimension_key.keys())):
        if text[-2].isdigit():
            text = "{} {}".format(text[:-1], _dimension_key[text[-1:]])
        elif text[-3].isdigit():
            text = "{} {}".format(text[:-2], _dimension_key[text[-2:]])
    return text


def normalize_letters_and_numbers(text):
    text = re.sub(_hardware_re, _expand_hardware, text)
    text = re.sub(_dimension_re, _expand_dimension, text)
    text = re.sub(_letters_and_numbers_re, _expand_letters_and_numbers, text)
    return text
