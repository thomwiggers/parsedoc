# -*- coding: utf-8 -*-
"""
Parsed blocks of PHP objects with attached comments
"""
from __future__ import unicode_literals


class PHPObject(object):
    """Base PHP object"""

    template = "{name}\n```{comment}```"

    def __init__(self, name, comment, contains=None):
        """
        Create a new instance of a PHPObject

        PHP Objects have a name, comment and may contain
        other objects
        """
        self.name = name
        self.comment = comment
        self.contains = contains or []

    def __str__(self):
        output = self.template.format(name=self.name,
                                      comment=self.comment)
        for item in self.contains:
            output += str(item)

        return output

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
    template = "## {name}\n```{comment}```"


class PHPFunction(PHPObject):
    """PHP Function"""
    template = "### {name}\n```{comment}```"
