import numpy as np
from research_RegEx import regex_symbol as rs
from research_RegEx import regex_tree as rt


class NDFA:
    def __init__(self, rg_tree: rt.RegExTree):
        nb_states = count_states(rg_tree)
        self.transition_table = np.full((nb_states, 256), -1, dtype=int)
        self.epsilon_transitions = np.full(nb_states, None, dtype=list)
        self.accept = np.full(nb_states, False, dtype=bool)
        self.sz = 0
        self.end = -1

    def to_string(self) -> str:
        result = "Initial state: 0\nFinal state: " + str(self.end) + "\nTransition list:\n"
        i = 0
        for e in self.epsilon_transitions:
            if e is not None:
                for state in e:
                    result += "  " + str(i) + " -- epsilon --> " + str(state) + "\n"
            i += 1
        for i in range(len(self.transition_table)):
            for col in range(256):
                if self.transition_table[i][col] != -1:
                    result += "  " + str(i) + " -- " + chr(col) + " --> " + str(self.transition_table[i][col]) + "\n"
        return result

    def increment_size(self, *, n=1):
        self.sz += n

    def __str__(self):
        return self.to_string()


def count_states(rg_tree: rt.RegExTree):
    succ = 0
    for sub_t in rg_tree.sub_trees:
        succ += count_states(sub_t)

    r = rg_tree.root
    if r == rs.DOT:
        return succ - 1
    elif r == rs.ETOILE:
        return succ + 2
    elif r == rs.ALTERN:
        return succ + 2
    else:
        return succ + 2
