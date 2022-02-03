from regex_tree import RegExTree
from ndfa import NDFA
from dfa import DFA

from research.regex.regex_parser import parse_expression
from research.regex.ndfa_parser import parse_ndfa
from research.regex.dfa_parser import parse_dfa, minimize_dfa


def generate_dfa(expression: str) -> DFA:
    rt = parse_expression(expression)
    ndfa = parse_ndfa(rt)
    dfa = parse_dfa(ndfa)
    minimize_dfa(dfa)
    return dfa
