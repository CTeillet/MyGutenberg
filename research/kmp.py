import numpy as np


def kmp(pat, text, co):
    if len(text) == 0:
        return -1
    i = 0
    j = 0
    lens = text.length()
    lenp = pat.length()
    while i < lens and j < lenp:
        if text.charAt(i) == pat.charAt(j):
            i += 1
            j += 1
        elif j == 0:
            i += 1
        else:
            j = co[j - 1] + 1
    if j == lenp:
        return i - lenp
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
