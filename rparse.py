#!/usr/bin/env python
# Copyright 2015, Dmitry Veselov

from plyplus import Grammar


__all__ = [
    "parse"
]


grammar = Grammar(r"""
start : package* ;


package: name vspec? ;

name : string ;

vspec : comparison version (',' comparison version)* ;
comparison : '<' | '<=' | '!=' | '==' | '>=' | '>' | '~=' | '===' ;
version : string ;

@string : '[-A-Za-z0-9_.]+' ;

SPACES: '[ \t\n]+' (%ignore) (%newline);
""")


def parse(requirements, g=grammar):
    """
    Parses given requirements and yields its AST.
    """
    return g.parse(requirements)
