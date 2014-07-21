# -*- coding: utf-8 -*-
from unittest import TestCase

from parsedoc.parser import *
from parsedoc import blocks


def test_file_commented_function_commented():
    result = parse_file("foo.php", """<?php
/**
 * File comment
 */

/**
 * Function 1 comment
 */
function foo_function($arg1, $arg2) {
    // bar
}
""")
    assert type(result) == blocks.PHPFile
    assert result.name == "foo.php"
    assert "File comment" in result.comment
    assert "Function 1 comment" not in result.comment
    assert len(result.contains) == 1  # one function
    function = result.contains[0]
    assert function.name == "foo_function($arg1, $arg2)"
    assert "Function 1 comment" in function.comment
    assert len(function.contains) == 0

def test_file_uncommented():
    result = parse_file("bar.php", """<?
function hi() {
    return "Hello World";
}""")
    assert type(result) == blocks.PHPFile
    assert result.name == "bar.php"
    assert result.comment is None
    assert len(result.contains) == 1

def test_get_file_comment():
    result, rest = get_file_comment("""<?php
/**
 * File comment
 */

blabla""")
    assert "File comment" in result
    assert "blabla" in rest

def test_get_file_comment_no_comment():
    result, rest = get_file_comment("<?php\nfunction foo(){};")
    assert result is None
    assert "function foo(){};" == rest

def test_get_file_comment_no_php():
    result, rest = get_file_comment("<? """"
/**
 * File comment
 */

blabla""")
    assert "File comment" in result
    assert "blabla" in rest

def test_get_file_comment_empty_rest():
    result, rest = get_file_comment("""<?php
/**
 * File comment
 */""")
    assert "File comment" in result
    assert rest == ""
