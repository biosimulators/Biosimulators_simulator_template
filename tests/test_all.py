""" Tests of the command-line interface

:Author: Author name <email@organization>
:Date: YYYY-MM-DD
:Copyright: YYYY, Owner
:License: <License, e.g., MIT>
"""
from biosimulators_utils.simulator.exec import exec_sedml_docs_in_archive_with_containerized_simulator
from my_simulator import __main__
from my_simulator import core
from unittest import mock
import numpy
import os
import shutil
import tempfile
import unittest


class CliTestCase(unittest.TestCase):
    EXAMPLE_ARCHIVE_FILENAME = os.path.join(os.path.dirname(__file__), 'fixtures', 'BIOMD0000000297.omex')
    DOCKER_IMAGE = '<registry>/<organization>/<repository>'

    def setUp(self):
        self.dirname = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.dirname)

    def test_raw_cli(self):
        with mock.patch('sys.argv', ['', '--help']):
            with self.assertRaises(SystemExit) as context:
                __main__.main()
                self.assertRegex(context.Exception, 'usage: ')

    def test_exec_sedml_docs_in_combine_archive(self):
        core.exec_sedml_docs_in_combine_archive(self.EXAMPLE_ARCHIVE_FILENAME, self.dirname)
        self.assert_outputs_created()

    def test_exec_sedml_docs_in_combine_archive_with_cli(self):
        with __main__.App(argv=['-i', self.EXAMPLE_ARCHIVE_FILENAME, '-o', self.dirname]) as app:
            app.run()
        self.assert_outputs_created()

    def test_exec_sedml_docs_in_combine_archive_with_docker_image(self):
        exec_sedml_docs_in_archive_with_containerized_simulator(
            self.EXAMPLE_ARCHIVE_FILENAME, self.out_dir, self.DOCKER_IMAGE, pull_docker_image=False)
        self.assert_outputs_created()

    def assert_outputs_created(self, dirname):
        self.assertEqual(set(os.listdir(dirname)), set(['reports.h5']))
