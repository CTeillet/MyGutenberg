CONCAT = 0xC04CA7
ETOILE = 0xE7011E
ALTERN = 0xA17E54
PROTECTION = 0xBADDAD

PARENTHESEOUVRANT = 0x16641664
PARENTHESEFERMANT = 0x51515151
DOT = 0xD07


def char_to_root(c: chr) -> int:
    if c == '.':
        return DOT
    elif c == '*':
        return ETOILE
    if c == '|':
        return ALTERN
    if c == '(':
        print('PARENTHESE OUVRANTE')
        return PARENTHESEOUVRANT
    if c == ')':
        print('PARENTHESE FERMANTE')
        return PARENTHESEFERMANT
    return ord(c)
