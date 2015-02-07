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


package : name extras? specs?;
name : string ;

specs : comparison version (',' comparison version)* ;
comparison : '<' | '<=' | '!=' | '==' | '>=' | '>' | '~=' | '===' ;
version : string ;

extras : '\[' (extra (',' extra)*)? '\]' ;
extra : string ;

@string : '[-A-Za-z0-9_\.]+' ;

SPACES: '[ \t\n]+' (%ignore) (%newline);
""")


class Requirement(object):

    def __init__(self, name=None, extras=None, specs=None):
        self.name = name
        self.extras = extras
        self.specs = specs

    def __str__(self):
        return "<{0}(name='{1}'>".format(self.__class__.__name__, self.name)


class RTransformer(STransformer):

    def package(self, node):
        requirement = Requirement()
        for key, value in node.tail:
            setattr(requirement, key, value)
        return requirement

    def name(self, node):
        return ("name", node.tail[0])

    def specs(self, node):
        comparisons, versions = node.tail[0::2], node.tail[1::2]
        return ("specs", list(zip(comparisons, versions)))

    def comparison(self, node):
        return node.tail[0]

    def version(self, node):
        return node.tail[0]

    def extras(self, node):
        return ("extras", [name for name in node.tail])

    def extra(self, node):
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
