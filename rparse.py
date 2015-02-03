#!/usr/bin/env python
# Copyright 2015, Dmitry Veselov

from plyplus import Grammar, ParseError
try:
    # Python 2.x and pypy
    from itertools import imap as map
except ImportError:
    # Python 3.x already have lazy map
    pass


__all__ = [
    "parse"
]


grammar = Grammar(r"""
start : package ;


package: name vspec? ;

name : string ;

vspec : comparison version (',' comparison version)* ;
comparison : '<' | '<=' | '!=' | '==' | '>=' | '>' | '~=' | '===' ;
version : string ;

@string : '[-A-Za-z0-9_.]+' ;

SPACES: '[ \t\n]+' (%ignore) (%newline);
""")


def _parse(requirement, g=grammar):
    try:
        return g.parse(requirement)
    except ParseError:
        message = "Invalid requirement: '{0}'" \
                  .format(requirement.strip())
        raise ValueError(message)


def parse(requirements):
    """
    Parses given requirements line-by-line.
    """
    return map(_parse, filter(None, requirements.splitlines()))
