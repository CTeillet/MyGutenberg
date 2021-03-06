import numpy as np


class TempDFA:
    def __init__(self, size_max: int):
        self.grouped_states = []
        self.accept = np.full(size_max, False, dtype=bool)
        self.transitions = np.full((size_max, 256), None, dtype=set)


class DFA:
    def __init__(self, dfa: TempDFA):
        self.size = len(dfa.grouped_states)
        self.accept = np.array(dfa.accept[:self.size], dtype=bool)
        self.transitions = np.full((self.size, 256), -1, dtype=int)
        for i in range(self.size):
            for j in range(256):
                if dfa.transitions[i][j] is not None:
                    s = dfa.grouped_states.index(dfa.transitions[i][j])
                    self.transitions[i][j] = s

    def __str__(self):
        res = "Initial state: 0\nFinal state(s): "
        for i in range(self.size):
            if self.accept[i]:
                res += str(i) + ", "
        res += "\nTransition list:\n"

        for i in range(self.size):
            for col in range(256):
                if self.transitions[i][col] != -1:
                    res += str(i) + " -- " + chr(col) + " --> " + str(self.transitions[i][col]) + "\n"
        return res

    def apply(self, string: str) -> bool:
        dfa_index = 0
        begin_dfa = 0
        if self.accept[dfa_index]:
            return True
        i = 0
        while i < len(string):
            s = string[i]
            if ord(s) > 255:
                dfa_index = 0
                i = begin_dfa
                begin_dfa += 1
            else:

                val_transition = self.transitions[dfa_index][ord(s)]
                if val_transition != -1:
                    if dfa_index == 0:
                        begin_dfa = i + 1
                    dfa_index = val_transition
                    if self.accept[dfa_index]:
                        return True
                    i += 1
                else:
                    dfa_index = 0
                    i = begin_dfa
                    begin_dfa += 1

        return False

    def apply_simple(self, string: str):
        dfa_index = 0
        if self.accept[dfa_index]:
            return True

        for s in string:
            if ord(s) > 255:
                dfa_index = 0

            else:
                val_transition = self.transitions[dfa_index][ord(s)]
                if val_transition != -1:
                    dfa_index = val_transition
                    if self.accept[dfa_index]:
                        return True
                elif dfa_index != 0:
                    dfa_index = 0
                    val_transition = self.transitions[dfa_index][ord(s)]
                    if val_transition != -1:
                        dfa_index = val_transition
                        if self.accept[dfa_index]:
                            return True

        return False
