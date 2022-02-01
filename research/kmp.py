import numpy as np


def kmp(pat, text, co):
    if len(text) == 0:
        return -1
    i = 0
    j = 0
    len_str = text.length()
    len_pat = pat.length()
    while i < len_str and j < len_pat:
        if text.charAt(i) == pat.charAt(j):
            i += 1
            j += 1
        elif j == 0:
            i += 1
        else:
            j = co[j - 1] + 1
    if j == len_pat:
        return i - len_pat
    return -1


def generate_co(target):
    co = np.zeros(len(target))
    n = len(target)
    co[0] = -1
    for i in range(1, n):
        j = co[i - 1]
        while target[i] != target[j + 1] and j >= 0:
            j = co[j]
        if target[i] == target[j + 1]:
            co[i] = j + 1
        else:
            co[i] = -1

    return co
