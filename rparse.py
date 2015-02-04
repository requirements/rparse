#!/usr/bin/env python
# Copyright 2015, Dmitry Veselov
from re import sub
from plyplus import Grammar, STransformer, \
                    ParseError, TokenizeError
try:
    # Python 2.x and pypy
    from itertools import imap as map
    from itertools import ifilter as filter
except ImportError:
    # Python 3.x already have lazy map
    pass


__all__ = [
    "parse"
]


grammar = Grammar(r"""
@start : package ;


package : name vspec? ;

name : string ;
vspec : comparison version (',' comparison version)* ;
comparison : '<' | '<=' | '!=' | '==' | '>=' | '>' | '~=' | '===' ;
version : string ;

@string : '[-A-Za-z0-9_\.]+' ;

SPACES: '[ \t\n]+' (%ignore) (%newline);
""")


class RTransformer(STransformer):

    def package(self, node):
        if len(node.tail) == 2:
            name, vspec = node.tail
        else:
            name, vspec = node.tail[0], None
        return name, vspec

    def name(self, node):
        return node.tail[0]

    def vspec(self, node):
        comparisons, versions = node.tail[0::2], node.tail[1::2]
        return list(zip(comparisons, versions))

    def comparison(self, node):
        return node.tail[0]

    def version(self, node):
        return node.tail[0]


def _parse(requirement, g=grammar):
    requirement = sub(r"#.*", "", requirement)
    try:
        if requirement:
            return g.parse(requirement)
        else:
            return None
    except (ParseError, TokenizeError):
        message = "Invalid requirements line: '{0}'" \
                  .format(requirement.strip())
        raise ValueError(message)


def parse(requirements):
    """
    Parses given requirements line-by-line.
    """
    transformer = RTransformer()
    return map(transformer.transform, filter(None, map(_parse, requirements.splitlines())))
