# -*- coding: utf-8 -*-
"""Tests for the parser"""
# Disable QA because test cases might use tabs/long lines
# flake8: noqa
from __future__ import unicode_literals

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
    assert result.comment is ""
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
    result = parse_file(
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
    block = result.contains[0]
    assert type(block) == blocks.PHPClass
    assert "Test Class" in block.comment
    assert "TestClass" in block.name
    assert len(block.contains) == 1
    block = block.contains[0]
    assert type(block) == blocks.PHPFunction
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


def test_function_private():
    result, _ = get_function_or_class(
        """
        /**
         * comment
         */
        public static function test_function () {
            //content
        }
        """)
    assert type(result) == blocks.PHPFunction
    assert "test_function" in result.name
    assert "comment" in result.comment
    assert len(result.contains) == 0


def test_function_caps():
    result, _ = get_function_or_class(
        """
        /**
         * comment
         */
        public static function TEST_FUNCTION () {
            //content
        }
        """)
    assert type(result) == blocks.PHPFunction
    assert "TEST_FUNCTION" in result.name
    assert "comment" in result.comment
    assert len(result.contains) == 0


def test_class_extended_abstract():
    result, _ = get_function_or_class(
        """
        /**
         * Comment
         */
        abstract class FooClass extends FooAbstract {
          // comment
        }
        """)
    assert type(result) == blocks.PHPClass
    assert "FooClass" in result.name
    assert "Comment" in result.comment
    assert len(result.contains) == 0


def test_abstract_function():
    result, _ = get_function_or_class(
        """
        /**
         * comment
         */
        abstract static function foo_function($args);
        """)
    assert type(result) == blocks.PHPFunction
    assert "foo_function" in result.name
    assert "comment" in result.comment
    assert len(result.contains) == 0


def test_function_with_body():
    """Test a function with a body

    The below code is part of Gazelle.
    """
    result, _ = get_function_or_class(
       r"""
    /**
     * @param string $application
     * @param string $event
     * @param string $description
     * @param string $url
     * @param int    $priority
     * @param bool   $apiKeys
     *
     * @return bool|mixed|SimpleXMLElement|string
     */
    public function notify($application = '', $event = '', $description = '', $url = '', $priority = 0, $apiKeys = false)
    {
        if (empty($application) || empty($event) || empty($description)) {
            return $this->error('you must supply a application name, event and long desc');
        }

        $post = array('application' => substr($application, 0, 256),
                      'event'       => substr($event, 0, 1000),
                      'description' => substr($description, 0, 10000),
                      'priority'    => $priority
        );
		if (!empty($url)) {
			$post['url'] = substr($url, 0, 2000);
		}
        if ($this->devKey) {
            $post['developerkey'] = $this->devKey;
        }

        if ($apiKeys !== false) {
            $post['apikey'] = $apiKeys;
        } else {
            $post['apikey'] = $this->apiKey;
        }

        return $this->makeApiCall(self::LIB_NMA_NOTIFY, $post, 'POST');
    }
        """)

    assert type(result) == blocks.PHPFunction
    assert "application" in result.comment
    assert "event" in result.comment
    assert "notify" in result.name
    assert "if (empty" not in result.name
