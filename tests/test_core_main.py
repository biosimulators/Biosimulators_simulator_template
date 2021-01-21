""" Tests of the command-line interface

:Author: Author name <email@organization>
:Date: YYYY-MM-DD
:Copyright: YYYY, Owner
:License: <License, e.g., MIT>
"""

from biosimulators_utils.combine import data_model as combine_data_model
from biosimulators_utils.combine.io import CombineArchiveWriter
from biosimulators_utils.report import data_model as report_data_model
from biosimulators_utils.report.io import ReportReader
from biosimulators_utils.sedml import data_model as sedml_data_model
from biosimulators_utils.simulator.exec import exec_sedml_docs_in_archive_with_containerized_simulator
from biosimulators_utils.simulator.specs import gen_algorithms_from_specs
from my_simulator import __main__
from my_simulator.core import exec_sed_task, exec_sedml_docs_in_combine_archive
from unittest import mock
import numpy
import os
import shutil
import tempfile
import unittest


class CoreTestCase(unittest.TestCase):
    EXAMPLE_MODEL_FILENAME = os.path.join(os.path.dirname(__file__), 'fixtures', 'model.xml')
    EXAMPLE_ARCHIVE_FILENAME = os.path.join(os.path.dirname(__file__), 'fixtures', 'BIOMD0000000297.omex')
    DOCKER_IMAGE = '<registry>/<organization>/<repository>:latest'

    def setUp(self):
        self.dirname = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.dirname)

    def test_exec_sed_task(self):
        task = sedml_data_model.Task(
            model=sedml_data_model.Model(
                source=self.EXAMPLE_MODEL_FILENAME,
                language=sedml_data_model.ModelLanguage.SBML.value,
                changes=[],
            ),
            simulation=sedml_data_model.UniformTimeCourseSimulation(
                algorithm=sedml_data_model.Algorithm(
                    kisao_id='KISAO_0000560',
                    changes=[
                        sedml_data_model.AlgorithmParameterChange(
                            kisao_id='KISAO_0000209',
                            new_value='2e-6',
                        ),
                    ],
                ),
                initial_time=0.,
                output_start_time=10.,
                output_end_time=20.,
                number_of_points=20,
            ),
        )

        variables = [
            sedml_data_model.Variable(id='time', symbol=sedml_data_model.Symbol.time, task=task),
            sedml_data_model.Variable(id='A', target="/sbml:sbml/sbml:model/sbml:listOfSpecies/sbml:species[@id='A']", task=task),
            sedml_data_model.Variable(id='C', target='/sbml:sbml/sbml:model/sbml:listOfSpecies/sbml:species[@id="C"]', task=task),
            sedml_data_model.Variable(id='DA', target="/sbml:sbml/sbml:model/sbml:listOfSpecies/sbml:species[@id='DA']", task=task),
        ]

        variable_results = exec_sed_task(task, variables)

        self.assertTrue(sorted(variable_results.keys()), sorted([var.id for var in variables]))
        self.assertEqual(variable_results[variables[0].id].shape, (task.simulation.number_of_points + 1,))
        numpy.testing.assert_almost_equal(
            variable_results['time'],
            numpy.linspace(task.simulation.output_start_time, task.simulation.output_end_time, task.simulation.number_of_points + 1),
        )

        for results in variable_results.values():
            self.assertFalse(numpy.any(numpy.isnan(results)))

    def test_exec_sedml_docs_in_combine_archive(self):
        exec_sedml_docs_in_combine_archive(self.EXAMPLE_ARCHIVE_FILENAME, self.dirname)
        self.assert_outputs_created()

    def test_exec_sedml_docs_in_combine_archive_with_continuous_model_all_algorithms(self):
        for alg in gen_algorithms_from_specs(os.path.join(os.path.dirname(__file__), '..', 'biosimulators.json')).values():
            doc, archive_filename = self._build_combine_archive(algorithm=alg,
                                                                orig_model_filename='model.xml',
                                                                var_targets=[None, 'A', 'C', 'DA'])

            out_dir = os.path.join(self.dirname, alg.kisao_id)
            exec_sedml_docs_in_combine_archive(archive_filename, out_dir,
                                               report_formats=[
                                                   report_data_model.ReportFormat.h5,
                                                   report_data_model.ReportFormat.csv,
                                               ],
                                               bundle_outputs=True,
                                               keep_individual_outputs=True)
            self._assert_combine_archive_outputs(doc, out_dir)

    def _build_combine_archive(self, algorithm=None, orig_model_filename='model.xml', var_targets=[None, 'A', 'C', 'DA']):
        # build SED document with algorithm
        doc = self._build_sed_doc(algorithm=algorithm)

        # build COMBINE archive with SED document
        archive = combine_data_model.CombineArchive()

        # save COMBINE archive to file
        archive_dirname = os.path.join(self.dirname, 'archive')
        archive_filename = os.path.join(self.dirname, 'archive.omex')
        CombineArchiveWriter().run(archive, archive_dirname, archive_filename)

        # return SED document and path to COMBINE archive
        return (doc, archive_filename)

    def _build_sed_doc(self, algorithm=None):
        # build SED document that uses the algorithm
        doc = sedml_data_model.SedDocument()
        return doc

    def _assert_combine_archive_outputs(self, doc, out_dir):
        # read the report of the results of the execution of the COMBINE archive
        report = doc.outputs[0]
        report_results = ReportReader().run(report, out_dir, 'simulation_1.sedml/simulation_1', format=report_data_model.ReportFormat.h5)

        # assert that the execution of the archive produced the expected results
        expected_report_results = report_data_model.DataSetResults({})
        for data_set in report.data_sets:
            numpy.testing.assert_almost_equal(report_results[data_set.id], expected_report_results[data_set.id])

    def test_exec_sedml_docs_in_combine_archive_with_cli(self):
        with __main__.App(argv=['-i', self.EXAMPLE_ARCHIVE_FILENAME, '-o', self.dirname]) as app:
            app.run()
        self.assert_outputs_created()

    def test_exec_sedml_docs_in_combine_archive_with_docker_image(self):
        exec_sedml_docs_in_archive_with_containerized_simulator(
            self.EXAMPLE_ARCHIVE_FILENAME, self.out_dir, self.DOCKER_IMAGE, pull_docker_image=False)
        self.assert_outputs_created()

    def assert_outputs_created(self, dirname):
        self.assertTrue(os.path.isfile(os.path.join(dirname, 'reports.h5')))

        report = sedml_data_model.Report(
            data_sets=[
                sedml_data_model.DataSet(id='time', label='time'),
            ]
        )

        report_results = ReportReader().run(report, dirname, 'simulation_1.sedml/simulation_1', format=report_data_model.ReportFormat.h5)

        self.assertEqual(len(report_results[report.data_sets[0].id]), 100 + 1)
        numpy.testing.assert_almost_equal(
            report_results[report.data_sets[0].id],
            numpy.linspace(0., 100., 100 + 1),
        )

        for data_set_result in report_results.values():
            self.assertFalse(numpy.any(numpy.isnan(data_set_result)))

    def test_raw_cli(self):
        with mock.patch('sys.argv', ['', '--help']):
            with self.assertRaises(SystemExit) as context:
                __main__.main()
                self.assertRegex(context.Exception, 'usage: ')
