import importlib
import sys
import unittest
from unittest import mock


class CliTests(unittest.TestCase):

    def tearDown(self):
        sys.modules.pop('shodan.__main__', None)

    def test_cli_imports_without_pkg_resources(self):
        with mock.patch.dict(sys.modules, {'pkg_resources': None}):
            cli = importlib.import_module('shodan.__main__')

        self.assertTrue(callable(cli.main))


if __name__ == '__main__':
    unittest.main()
