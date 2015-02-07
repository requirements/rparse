#!/usr/bin/env python
# Copyright 2015, Dmitry Veselov
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


package : name extras? specs? comment?;
name : string ;

specs : comparison version (',' comparison version)* ;
comparison : '<' | '<=' | '!=' | '==' | '>=' | '>' | '~=' | '===' ;
version : string ;

extras : '\[' (extra (',' extra)*)? '\]' ;
extra : string ;

comment : '\#.+' ;

@string : '[-A-Za-z0-9_\.]+' ;

SPACES: '[ \t\n]+' (%ignore) (%newline);
""")


class Requirement(object):

    def __init__(self, name=None, extras=None, specs=None, comment=None):
        self.name = name
        self.extras = extras
        self.specs = specs
        self.comment = comment

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

    def comment(self, node):
        return ("comment", " ".join([word for word in node.tail]))

    def comment_content(self, node):
        return node.tail[0]


def _parse(line, g=grammar):
    line = line.strip()
    if line.startswith("#"):
        return None
    try:
        if line:
            return g.parse(line)
        else:
            return None
    except (ParseError, TokenizeError):
        message = "Invalid requirements line: '{0}'".format(line)
        raise ValueError(message)


def parse(requirements):
    """
    Parses given requirements line-by-line.
    """
    transformer = RTransformer()
    return map(transformer.transform, filter(None, map(_parse, requirements.splitlines())))
