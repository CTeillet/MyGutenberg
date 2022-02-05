from dfa import DFA

from ndfa import count_states
from research.regex.regex_parser import parse_expression
from research.regex.ndfa_parser import parse_ndfa
from research.regex.dfa_parser import parse_dfa, minimize_dfa


def generate_dfa(expression: str) -> DFA:
    rt = parse_expression(expression)
    print('rt', rt)
    ndfa = parse_ndfa(rt)
    print('ndfa', ndfa)
    dfa = parse_dfa(ndfa)
    print('dfa', dfa)
    minimize_dfa(dfa)
    print('minimized dfa', dfa)
    return dfa


generate_dfa("a|bc*")
