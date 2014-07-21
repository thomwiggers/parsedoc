# -*- coding: utf-8 -*-
"""
Parse PHP files to get comment structures

"""
from __future__ import unicode_literals, print_function, absolute_import
import re
import logging

from .blocks import *


def parse_file(file_name, file_contents):
    """Parse a file into blocks of objects with comments"""
    file_comment, file_contents = get_file_comment(file_contents)
    return PHPFile(file_name, file_comment)

def get_file_comment(file_contents):
    """Get a comment from the start of a php file and return the rest"""
    file_comment = None
    # Find any comment at the start of the file
    regexp = re.compile(r"""
        ^\s*<\?(php)?\s*\n          # File start
        (?P<docblock>/\*\*.*?\*/)?  # documentation on line 2
        (?P<rest>.*)$               # Rest of the file
        """, re.VERBOSE | re.DOTALL)
    result = regexp.match(file_contents)
    if result:
        file_comment = result.group('docblock')
        logging.debug("Found comment: {}".format(file_comment))

    return file_comment, result.group('rest')
