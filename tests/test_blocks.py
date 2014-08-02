# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from parsedoc.blocks import PHPFile, PHPClass, PHPFunction


def test_PHPFile():
    f = PHPFile('foo', 'bar')
    assert f.name == 'foo'
    assert f.comment == 'bar'
    assert 'foo' in str(f)
    assert 'bar' in str(f)


def test_PHPFile_contains():
    f = PHPClass('foo', 'bar')
    fb = PHPFile('baz', 'bat', [f])
    assert fb.name == 'baz'
    assert fb.comment == 'bat'
    assert 'bar' in str(fb)
    assert 'foo' in str(fb)


def test_PHPClass_contains():
    f = PHPFunction('foo', 'bar')
    fb = PHPClass('baz', 'bat', [f])
    assert fb.name == 'baz'
    assert fb.comment == 'bat'
    assert 'bar' in str(fb)
    assert 'foo' in str(fb)
