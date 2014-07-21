#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''parsedoc

Parses PHP files to extract docblock comments to Markdown files

Usage:
  parsedoc <file>
  parsedoc -h | --help
  parsedoc --version

Options:
  -h --help     Show this screen.
  --version     Show version.
'''

from __future__ import unicode_literals, print_function
from docopt import docopt

__version__ = "0.1.0"
__author__ = "Thom Wiggers"
__license__ = "GPLv3"


def main():
    '''Main entry point for the parsedoc CLI.'''
    args = docopt(__doc__, version=__version__)
    print(args)

if __name__ == '__main__':
    main()
