import sys

from regex import RegEx
from .errors import SyntaxError
from parse_regex.lexer import lexer
from parse_regex.parser import parser

__all__ = ["parse_regex", "SyntaxError"]

def parse_regex(regex_str: str) -> RegEx:
    
    lexer.input(regex_str)

    # Tokenize
    while True:
        tok = lexer.token()
        if not tok:
            break      # No more input
        print(tok)

    return parser.parse(regex_str)