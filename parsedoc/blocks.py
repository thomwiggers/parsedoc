# -*- coding: utf-8 -*-
"""
Parsed blocks of PHP objects with attached comments
"""
from __future__ import unicode_literals, print_function

class PHPObject(object):
    """Base PHP object"""

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
        return self.__unicode__()

    def __unicode__(self):
        return """
        {name}
        ======
        {comment}""".format(name=self.name, comment=self.comment)

class PHPFile(PHPObject):
    """PHP File
    
    May contain classes and functions
    """
    pass

class PHPClass(PHPObject):
    """PHP class

    May contain functions
    """
    pass

class PHPFunction(PHPObject):
    """PHP Function"""
    pass
