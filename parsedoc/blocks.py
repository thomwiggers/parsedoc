# -*- coding: utf-8 -*-
"""
Parsed blocks of PHP objects with attached comments
"""
from __future__ import unicode_literals


class PHPObject(object):
    """Base PHP object"""

    template = "# {name}\n```\n{comment}```\n\n"

    def __init__(self, name, comment, contains=None):
        """
        Create a new instance of a PHPObject

        PHP Objects have a name, comment and may contain
        other objects
        """
        self.name = name.strip().rstrip('{').strip()
        self.comment = ""
        if comment is not None:
            comment_lines = comment.split('\n')
            for line in comment_lines:
                self.comment += ' ' + line.strip() + '\n'
            self.comment = self.comment.strip()
        self.contains = contains or []

    def __str__(self):
        output = self.template.format(name=self.name,
                                      comment=self.comment)
        for item in self.contains:
            output += str(item)

        return output

    def __repr__(self):
        return "<class '{}', name='{}'>".format(self.__class__.__name__,
                                                self.name)

    def __unicode__(self):
        return self.__str__()


class PHPFile(PHPObject):
    """PHP File

    May contain classes and functions
    """
    pass


class PHPClass(PHPObject):
    """PHP class

    May contain functions
    """
    template = "## {name}\n```\n{comment}\n```\n\n"


class PHPFunction(PHPObject):
    """PHP Function"""
    template = "### {name}\n```\n{comment}\n```\n\n"
