#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""parsedoc

Parses PHP files to extract docblock comments to Markdown files

Usage:
  parsedoc [options] <file>
  parsedoc -h | --help
  parsedoc --version

Options:
  -o FILE --output=FILE   Output to this file (default: filename.md)
  -h --help               Show this screen.
  --version               Show version.
"""

from __future__ import unicode_literals, print_function, with_statement
from docopt import docopt

from .parser import parse_file

import os.path

__version__ = "0.1.0"
__author__ = "Thom Wiggers"
__license__ = "GPLv3"


def main():
    """Main entry point for the parsedoc CLI."""
    args = docopt(__doc__, version=__version__)

    if os.path.isfile(args['<file>']):
        handle_file(args['<file>'], args.get('--output'))
    else:
        raise ValueError("Can't open directory {}".format(args['<file']))


def handle_file(filename, output):
    """Handle one file"""
    if not output:
        output = filename + '.md'

    with open(output, 'w') as outfile:
        with open(filename, 'r') as f:
            file_contents = f.read()
        parsed = parse_file(filename, file_contents)
        output = str(parsed)
        outfile.write(output)


if __name__ == '__main__':
    main()
