# -*- coding: utf-8 -*-
"""
Parse PHP files to get comment structures

"""
from __future__ import unicode_literals, print_function, absolute_import
import re
import logging

from .blocks import PHPFile, PHPClass, PHPFunction


def parse_file(file_name, file_contents):
    """Parse a file into blocks of objects with comments"""
    file_comment, file_contents = get_file_comment(file_contents)
    objects = []
    while file_contents:
        phpobject, file_contents = get_function_or_class(file_contents)
        if phpobject:
            objects.append(phpobject)
    return PHPFile(file_name, file_comment, objects)


def get_file_comment(file_contents):
    """Get a comment from the start of a php file and return the rest"""
    file_comment = None
    # Find any comment at the start of the file
    regexp = re.compile(r"""
        ^\s*<\?(php)?\s*\n          # File start
        (?P<docblock>/\*\*.*?\*/)?  # documentation on line 2
        [ ]*\n                      # newline
        (?P<rest>.*)$               # Rest of the file
        """, re.VERBOSE | re.DOTALL)
    result = regexp.match(file_contents)
    if result:
        file_comment = result.group('docblock')
        logging.debug("Found comment: {}".format(file_comment))
        return file_comment, result.group('rest').strip()
    else:
        return None, file_contents


def get_function_or_class(file_contents):
    """Get one function or class from file_contents"""
    regexp = re.compile(r"""
        .*?                            # Eat up everything that isn't a
                                       # function or class
        ((?P<docblock>/\*\*.*?\*/)     # find docblock
        [ ]*\n)?                       # eat space and newline
        [ ]*                           # eat any prefix spaces
        ((?P<function>                 # find a function
            (static|public|private|protected|[ ])*
            function .*?{          ) |
         (?P<class>class .*? {))       # or a class
        (?P<rest>.*)                   # rest of the file
        """, re.VERBOSE | re.DOTALL)
    result = regexp.match(file_contents)

    if not result:
        return None, ""

    if result.group('class'):
        return parse_class(result, file_contents)
    elif result.group('function'):
        comment = ""
        if result.group('docblock'):
            comment = result.group('docblock')
        return (PHPFunction(result.group('function'), comment),
                result.group('rest').strip())


def parse_class(result, file_contents):
    comment = ""
    if result.group('docblock'):
        comment = result.group('docblock')
    """Parse a class"""
    # find contents of class:
    stack = 1
    accum = ''
    for c in result.group('rest'):
        accum += c
        if c == '}':
            stack -= 1
        elif c == '{':
            stack += 1

        if stack == 0:
            break
    if len(accum) < len(result.group('rest')):
        rest = result.group('rest')[len(accum):]
    else:
        rest = ''
    class_contains = []
    while accum:
        block, accum = get_function_or_class(accum)
        if block:
            class_contains.append(block)
    return (PHPClass(result.group('class'), comment, class_contains),
            rest.strip())
