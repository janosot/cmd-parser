# pylint: disable=no-member,import-error

import unittest

from src.option_parser import Option, OptionParser

from decorators import with_argv, auto_parse


class TestPlainWithParameterless(unittest.TestCase):
    def setUp(self):
        self.parser = OptionParser(throw_on_error=True)

        self.option = Option("option", "o")

        self.parser.add_options(self.option)

    @with_argv(["plain1", "plain2", "plain3"])
    @auto_parse
    def test_only_plains_sets_correct_value(self):
        self.assertEqual(
            self.config.get_plain_args(),
            ["plain1", "plain2", "plain3"]
        )

    @with_argv(["plain1", "--option", "plain2", "plain3"])
    @auto_parse
    def test_mixed_ignores_options(self):
        self.assertEqual(
            self.config.get_plain_args(),
            ["plain1", "plain2", "plain3"]
        )

    @with_argv(["plain1", "--option", "plain2", "--", "plain3", "--option", "plain4"])
    @auto_parse
    def test_delimiter_ignores_optoins(self):
        self.assertEqual(
            self.config.get_plain_args(),
            ["plain1", "plain2", "plain3", "--option", "plain4"]
        )


class TestPlainWithParameterized(unittest.TestCase):
    def setUp(self):
        self.parser = OptionParser(throw_on_error=True)

        self.option = Option("option", "o")
        self.option.set_parameter_settings()

        self.parser.add_options(self.option)

    @with_argv(["plain1", "--option=option-parameter", "plain2", "plain3"])
    @auto_parse
    def test_mixed_ignores_options(self):
        self.assertEqual(
            self.config.get_plain_args(),
            ["plain1", "plain2", "plain3"]
        )

    @with_argv(["plain1", "--option=parameter", "--", "plain3", "--option", "parameter", "plain4"])
    @auto_parse
    def test_delimiter_ignores_options(self):
        self.assertEqual(
            self.config.get_plain_args(),
            ["plain1", "plain3", "--option", "parameter", "plain4"]
        )
