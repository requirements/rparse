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
    >>> requirements = "flask==0.10.1"
    >>> ast = parse(requirements)
    >>> list(ast.select("package > name *"))
    ['flask']
    >>> list(ast.select("package > vspec > comparison *"))
    ['==']
    >>> list(ast.select("package > vspec > version *"))
    ['0.10.1']
    """
    return g.parse(requirements)
