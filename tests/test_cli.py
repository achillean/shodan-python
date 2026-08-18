import importlib
import sys
import unittest
from types import ModuleType
from unittest import mock

from click.testing import CliRunner


class CliTests(unittest.TestCase):

    def test_plugins_load_from_legacy_entry_point_mapping(self):
        # Given the mapping returned by older importlib-metadata releases
        cli = importlib.import_module('shodan.__main__')
        plugin = object()

        with mock.patch('shodan.__main__.entry_points', return_value={'shodan.cli.plugins': (plugin,)}):
            # When the CLI discovers third-party plugins
            plugins = tuple(cli.iter_plugin_entry_points('shodan.cli.plugins'))

        # Then it returns the entries for the requested group
        self.assertEqual((plugin,), plugins)

    def test_version_reports_installed_distribution(self):
        # Given the installed Shodan CLI
        cli = importlib.import_module('shodan.__main__')

        # When its version command is invoked
        result = CliRunner().invoke(cli.main, ['version'])

        # Then it reports the installed distribution version
        self.assertEqual(0, result.exit_code, result.output)
        self.assertRegex(result.output.strip(), r'^\d+\.\d+\.\d+$')

    def test_help_renders_without_pkg_resources(self):
        # Given an isolated runtime where pkg_resources is unavailable
        previous = sys.modules.get('pkg_resources')
        sys.modules['pkg_resources'] = ModuleType('pkg_resources')
        sys.modules.pop('shodan.__main__', None)

        try:
            # When the CLI is imported and asked to render help
            try:
                cli = importlib.import_module('shodan.__main__')
            except ImportError as exc:
                self.fail('CLI import should not require pkg_resources: {}'.format(exc))
            result = CliRunner().invoke(cli.main, ['--help'])
        finally:
            sys.modules.pop('shodan.__main__', None)
            if previous is not None:
                sys.modules['pkg_resources'] = previous
            else:
                sys.modules.pop('pkg_resources', None)

        # Then help renders successfully through the real Click command
        self.assertEqual(0, result.exit_code, result.output)
        self.assertIn('Usage:', result.output)


if __name__ == '__main__':
    unittest.main()
