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



