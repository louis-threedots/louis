#! /usr/bin/python3
alphabet_dict = {
    'a': {'dots': [1, 0, 0, 0, 0, 0], 'pronunciation': 'ay'},
    'b': {'dots': [1, 1, 0, 0, 0, 0], 'pronunciation': 'b'},
    'c': {'dots': [1, 0, 0, 1, 0, 0], 'pronunciation': 'c'},
    'd': {'dots': [1, 0, 0, 1, 1, 0], 'pronunciation': 'd'},
    'e': {'dots': [1, 0, 0, 0, 1, 0], 'pronunciation': 'e'},
    'f': {'dots': [1, 1, 0, 1, 0, 0], 'pronunciation': 'f'},
    'g': {'dots': [1, 1, 0, 1, 1, 0], 'pronunciation': 'g'},
    'h': {'dots': [1, 1, 0, 0, 1, 0], 'pronunciation': 'h'},
    'i': {'dots': [0, 1, 0, 1, 0, 0], 'pronunciation': 'i'},
    'j': {'dots': [0, 1, 0, 1, 1, 0], 'pronunciation': 'j'},
    'k': {'dots': [1, 0, 1, 0, 0, 0], 'pronunciation': 'k'},
    'l': {'dots': [1, 1, 1, 0, 0, 0], 'pronunciation': 'l'},
    'm': {'dots': [1, 0, 1, 1, 0, 0], 'pronunciation': 'm'},
    'n': {'dots': [1, 0, 1, 1, 1, 0], 'pronunciation': 'n'},
    'o': {'dots': [1, 0, 1, 0, 1, 0], 'pronunciation': 'o'},
    'p': {'dots': [1, 1, 1, 1, 0, 0], 'pronunciation': 'p'},
    'q': {'dots': [1, 1, 1, 1, 1, 0], 'pronunciation': 'q'},
    'r': {'dots': [1, 1, 1, 0, 1, 0], 'pronunciation': 'r'},
    's': {'dots': [0, 1, 1, 1, 0, 0], 'pronunciation': 's'},
    't': {'dots': [0, 1, 1, 1, 1, 0], 'pronunciation': 't'},
    'u': {'dots': [1, 0, 1, 0, 0, 1], 'pronunciation': 'u'},
    'v': {'dots': [1, 1, 1, 0, 0, 1], 'pronunciation': 'v'},
    'w': {'dots': [0, 1, 0, 1, 1, 1], 'pronunciation': 'w'},
    'x': {'dots': [1, 0, 1, 1, 0, 1], 'pronunciation': 'x'},
    'y': {'dots': [1, 0, 1, 1, 1, 1], 'pronunciation': 'y'},
    'z': {'dots': [1, 0, 1, 0, 1, 1], 'pronunciation': 'z'},
}
punctuation_dict = {
    '.': {'dots': [0, 1, 0, 0, 1, 1], 'pronunciation': 'period'},
    ',': {'dots': [0, 1, 0, 0, 0, 0], 'pronunciation': 'comma'},
    ';': {'dots': [0, 1, 1, 0, 0, 0], 'pronunciation': 'semicolon'},
    ':': {'dots': [0, 1, 0, 0, 1, 0], 'pronunciation': 'colon'},
    '/': {'dots': [0, 0, 1, 1, 0, 0], 'pronunciation': 'slash'},
    '?': {'dots': [0, 1, 1, 0, 0, 1], 'pronunciation': 'question mark'},
    '!': {'dots': [0, 1, 1, 0, 1, 0], 'pronunciation': 'exclamation mark'},
    '@': {'dots': [0, 0, 1, 1, 1, 0], 'pronunciation': 'at symbol'},
    '#': {'dots': [0, 0, 1, 1, 1, 1], 'pronunciation': 'hash'},
    '+': {'dots': [0, 1, 1, 0, 1, 0], 'pronunciation': 'plus'},
    '-': {'dots': [0, 0, 1, 0, 0, 1], 'pronunciation': 'minus'},
    '*': {'dots': [0, 0, 1, 0, 1, 0], 'pronunciation': 'asterisk'},
    '<': {'dots': [1, 1, 0, 0, 0, 1], 'pronunciation': 'less than symbol'},
    '>': {'dots': [0, 0, 1, 1, 1, 0], 'pronunciation': 'greater than symbol'},
    '(': {'dots': [0, 1, 1, 0, 1, 1], 'pronunciation': 'left parenthesis'},
    ')': {'dots': [0, 1, 1, 0, 1, 1], 'pronunciation': 'right parenthesis'},
    '\'': {'dots': [0, 0, 1, 0, 0, 0], 'pronunciation': 'apostrophe'},
    '\"': {'dots': [0, 0, 1, 0, 0, 0], 'pronunciation': 'quotation mark'},
    ' ': {'dots': [0, 0, 0, 0, 0, 0], 'pronunciation': 'blank space'},
}
digit_dict = {
    '0': {'dots': [0, 1, 0, 1, 1, 0], 'pronunciation': 'zero'},
    '1': {'dots': [1, 0, 0, 0, 0, 0], 'pronunciation': 'one'},
    '2': {'dots': [1, 1, 0, 0, 0, 0], 'pronunciation': 'two'},
    '3': {'dots': [1, 0, 0, 1, 0, 0], 'pronunciation': 'three'},
    '4': {'dots': [1, 0, 0, 1, 1, 0], 'pronunciation': 'four'},
    '5': {'dots': [1, 0, 0, 0, 1, 0], 'pronunciation': 'five'},
    '6': {'dots': [1, 1, 0, 1, 0, 0], 'pronunciation': 'six'},
    '7': {'dots': [1, 1, 0, 1, 1, 0], 'pronunciation': 'seven'},
    '8': {'dots': [1, 1, 0, 0, 1, 0], 'pronunciation': 'eight'},
    '9': {'dots': [0, 1, 0, 1, 0, 0], 'pronunciation': 'nine'},
}
indicator_dict = {
    'CAPITAL': {'dots': [0, 0, 0, 0, 0, 1], 'pronunciation': 'capital'},
    'LETTER': {'dots': [0, 0, 0, 0, 1, 1], 'pronunciation': 'letter'},
    'NUMBER': {'dots': [0, 0, 1, 1, 1, 1], 'pronunciation': 'number'},
    'UNKNOWN': {'dots': [1, 1, 1, 1, 1, 1], 'display': 'unknown character'},
}
contraction_dict = {
    'ch': {'dots': [1, 0, 0, 0, 0, 1], 'pronunciation': 'ch'},
    'sh': {'dots': [1, 0, 0, 1, 0, 1], 'pronunciation': 'sh'},
    'th': {'dots': [1, 0, 0, 1, 1, 1], 'pronunciation': 'th'},
    'wh': {'dots': [1, 0, 0, 0, 1, 1], 'pronunciation': 'wh'},
    'ou': {'dots': [1, 1, 0, 0, 1, 1], 'pronunciation': 'ou'},
    'st': {'dots': [0, 0, 1, 1, 0, 0], 'pronunciation': 'st'},
    'gh': {'dots': [1, 1, 0, 0, 0, 1], 'pronunciation': 'gh'},
    'ed': {'dots': [1, 1, 0, 1, 0, 1], 'pronunciation': 'ed'},
    'er': {'dots': [1, 1, 0, 1, 1, 1], 'pronunciation': 'er'},
    'ow': {'dots': [0, 1, 0, 1, 0, 1], 'pronunciation': 'ow'},
    'ar': {'dots': [0, 0, 1, 1, 1, 0], 'pronunciation': 'ar'},
    'ing': {'dots': [0, 0, 1, 1, 0, 1], 'pronunciation': 'ing'},
}

character_dict = {**alphabet_dict, **digit_dict, **punctuation_dict, **indicator_dict, **contraction_dict}

degrees_small = {
    '000': [0, 180],
    '001': [22, 202], # 0.5
    '010': [45, 225],
    '101': [67, 247], # 0.5
    '011': [90, 270],
    '111': [112, 292], # 0.5
    '110': [135, 315],
    '100': [157, 337], # 0.5
}

degrees_big = {
    '000': [0, 120, 240],
    '001': [15, 135, 255],
    '010': [30, 150, 270],
    '101': [45, 165, 285],
    '011': [60, 180, 300],
    '111': [75, 195, 315],
    '110': [90, 210, 330],
    '100': [105, 225, 345],
}

def character_degrees(character):
    if character not in character_dict:
        list_of_pins = character_dict['UNKNOWN']['dots']
    else:
        list_of_pins = character_dict[character]['dots']
    first_three = list_of_pins[:3]
    second_three = list_of_pins[3:]
    first_three_str = ''.join(str(pin) for pin in first_three)
    second_three_str = ''.join(str(pin) for pin in second_three)

    return {'big': degrees_big[first_three_str], 'small': degrees_small[second_three_str]}
