# -*- coding: utf-8 -*-
from parsedoc.parser import parse_file, get_function_or_class, get_file_comment
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
    assert "foo_function($arg1, $arg2)" in function.name
    assert function.comment
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
    assert "function foo(){};" in rest


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
 */
    """)
    assert "File comment" in result
    assert rest == ""


def test_file_with_class():
    result, rest = parse_file(
        "foo.php",
        """<?php
        /**
         * File comment
         */

        /**
         * Test Class
         */
        class TestClass
        {
            /**
             * test function
             */
            function foo_function() {
                //content
            }
        }
        """)
    assert type(result) == blocks.PHPFile
    assert "File comment" in result.comment
    assert len(result.contains) == 1
    assert type(result.contains[0]) == blocks.PHPClass
    block = result.contains[0]
    assert "Test Class" in block.comment
    assert "TestClass" in block.name
    assert len(block.contains) == 1
    block = block.contains[0]
    assert "test function" in block.comment
    assert "foo_function" in block.name
    assert len(block.contains) == 0


def test_function_comment():
    result, rest = get_function_or_class(
        """
        /**
         * Function 1 comment
         */
        function foo_function() {
            // function body
        }
        """)
    assert type(result) == blocks.PHPFunction
    assert "foo_function" in result.name
    assert "Function 1 comment" in result.comment
    assert len(result.contains) == 0


def test_class_comment():
    result, _ = get_function_or_class(
        """
        /**
         * Class comment
         */
        class FooClass {

            /**
             * foo function
             */
            function foo_function () {
                // contents
            }
            // other class contents
        }
        """)
    assert type(result) == blocks.PHPClass
    assert "FooClass" in result.name
    assert "Class comment" in result.comment
    assert len(result.contains) == 1
    function = result.contains[0]
    assert type(function) == blocks.PHPFunction
    assert "foo_function" in function.name
    assert "foo function" in function.comment
    assert len(function.contains) == 0


def test_class_comment_two_functions():
    result, _ = get_function_or_class(
        """
        /**
         * Class comment
         */
        class FooClass {

            /**
             * foo function 1
             */
            function foo_function_1 () {
                // contents
            }
            /**
             * foo function 2
             */
            function foo_function_2 () {
                // contents
            }
           // other class contents
        }
        """)
    assert type(result) == blocks.PHPClass
    assert "FooClass" in result.name
    assert "Class comment" in result.comment
    assert len(result.contains) == 2
    function = result.contains[0]
    assert type(function) == blocks.PHPFunction
    assert "foo_function_1" in function.name
    assert "foo function 1" in function.comment
    assert len(function.contains) == 0
    function = result.contains[1]
    assert type(function) == blocks.PHPFunction
    assert "foo_function_2" in function.name
    assert "foo function 2" in function.comment
    assert len(function.contains) == 0


def test_class_comment_two_functions_one_uncommented():
    result, _ = get_function_or_class(
        """
        /**
         * Class comment
         */
        class FooClass {

            /**
             * foo function 1
             */
            function foo_function_1 () {
                // contents
            }
            function foo_function_2 () {
                // contents
            }
           // other class contents
        }
        """)
    assert type(result) == blocks.PHPClass
    assert "FooClass" in result.name
    assert "Class comment" in result.comment
    assert len(result.contains) == 2
    function = result.contains[0]
    assert type(function) == blocks.PHPFunction
    assert "foo_function_1" in function.name
    assert "foo function 1" in function.comment
    assert len(function.contains) == 0
    function = result.contains[1]
    assert type(function) == blocks.PHPFunction
    assert "foo_function_2" in function.name
    assert function.comment == ""


def test_class_comment_two_functions_class_uncommented():
    result, _ = get_function_or_class(
        """
        class FooClass {

            /**
             * foo function 1
             */
            function foo_function_1 () {
                // contents
            }
            function foo_function_2 () {
                // contents
            }
           // other class contents
        }
        """)
    assert type(result) == blocks.PHPClass
    assert "FooClass" in result.name
    assert result.comment == ""
    assert len(result.contains) == 2
    function = result.contains[0]
    assert type(function) == blocks.PHPFunction
    assert "foo_function_1" in function.name
    assert "foo function 1" in function.comment
    assert len(function.contains) == 0
    function = result.contains[1]
    assert type(function) == blocks.PHPFunction
    assert "foo_function_2" in function.name
    assert function.comment == ""
