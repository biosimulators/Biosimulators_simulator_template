""" Methods for executing SED tasks and saving their results

:Author: Author name <email@organization>
:Date: YYYY-MM-DD
:Copyright: YYYY, Owner
:License: <License, e.g., MIT>
"""

from .data_model import KISAO_METHOD_MAP
from biosimulators_utils.combine.exec import exec_sedml_docs_in_archive
from biosimulators_utils.log.data_model import CombineArchiveLog, TaskLog  # noqa: F401
from biosimulators_utils.plot.data_model import PlotFormat  # noqa: F401
from biosimulators_utils.report.data_model import ReportFormat, DataGeneratorVariableResults  # noqa: F401
from biosimulators_utils.sedml import validation
from biosimulators_utils.sedml.data_model import (Task, ModelLanguage, ModelAttributeChange,  # noqa: F401
                                                  UniformTimeCourseSimulation, DataGeneratorVariable)
from biosimulators_utils.sedml.exec import exec_sed_doc
from biosimulators_utils.sedml.utils import apply_changes_to_xml_model
from biosimulators_utils.utils.core import parse_value
from my_simulator import read_model, get_sed_variables_from_results
import functools

__all__ = ['exec_sedml_docs_in_combine_archive', 'exec_sed_task']


def exec_sedml_docs_in_combine_archive(archive_filename, out_dir,
                                       report_formats=None, plot_formats=None,
                                       bundle_outputs=None, keep_individual_outputs=None):
    """ Execute the SED tasks defined in a COMBINE/OMEX archive and save the outputs

    Args:
        archive_filename (:obj:`str`): path to COMBINE/OMEX archive
        out_dir (:obj:`str`): path to store the outputs of the archive

            * CSV: directory in which to save outputs to files
              ``{ out_dir }/{ relative-path-to-SED-ML-file-within-archive }/{ report.id }.csv``
            * HDF5: directory in which to save a single HDF5 file (``{ out_dir }/reports.h5``),
              with reports at keys ``{ relative-path-to-SED-ML-file-within-archive }/{ report.id }`` within the HDF5 file

        report_formats (:obj:`list` of :obj:`ReportFormat`, optional): report format (e.g., csv or h5)
        plot_formats (:obj:`list` of :obj:`PlotFormat`, optional): report format (e.g., pdf)
        bundle_outputs (:obj:`bool`, optional): if :obj:`True`, bundle outputs into archives for reports and plots
        keep_individual_outputs (:obj:`bool`, optional): if :obj:`True`, keep individual output files

    Returns:
        :obj:`CombineArchiveLog`: log
    """
    sed_doc_executer = functools.partial(exec_sed_doc, exec_sed_task)
    return exec_sedml_docs_in_archive(sed_doc_executer, archive_filename, out_dir,
                                      apply_xml_model_changes=True,
                                      report_formats=report_formats,
                                      plot_formats=plot_formats,
                                      bundle_outputs=bundle_outputs,
                                      keep_individual_outputs=keep_individual_outputs)


def exec_sed_task(task, variables, log=None):
    ''' Execute a task and save its results

    Args:
       task (:obj:`Task`): task
       variables (:obj:`list` of :obj:`DataGeneratorVariable`): variables that should be recorded
       log (:obj:`TaskLog`, optional): log for the task

    Returns:
        :obj:`tuple`:

            :obj:`DataGeneratorVariableResults`: results of variables
            :obj:`TaskLog`: log

    Raises:
        :obj:`ValueError`: if the task or an aspect of the task is not valid, or the requested output variables
            could not be recorded
        :obj:`NotImplementedError`: if the task is not of a supported type or involves an unsuported feature
    '''
    log = log or TaskLog()

    #############################################################
    # Validate the task. See utilities in :obj:`validation`.
    validation.validate_task(task)

    # Validate that the model is encoded in a supported language
    validation.validate_model_language(task.model.language, ModelLanguage.SBML)

    # Validate that the model changes are of the supported types
    validation.validate_model_change_types(task.model.changes, (ModelAttributeChange, ))

    # Validate that the simulation is a supported type of simulation
    validation.validate_simulation_type(task.simulation, (UniformTimeCourseSimulation, ))

    # If the simulation is a time course, check that the initial time, output start time, output end time, and number of points are valid
    validation.validate_uniform_time_course_simulation(task.simulation)

    # Check that the variables of the data generators are valid (have either a symbol or target)
    validation.validate_data_generator_variables(variables)

    # If the model is encoded in XML, check that the XPATHs for the variables are valid
    target_x_paths_ids = validation.validate_data_generator_variable_xpaths(variables, task.model.source, attr='id')

    # Check that the simulation tool can produce each variables -- the simulation tool supports each symbol and target

    #############################################################
    # Read the model located at `task.model.source`
    model = read_model(task.model.source, language=task.model.language)

    #############################################################
    # Apply the model changes specified by `task.model.changes`
    apply_changes_to_xml_model(changes=task.model.changes, in_model_filename=task.model.source, out_model_filename=task.model.source)

    #############################################################
    # Load the algorithm specified by `simulation.algorithm`
    simulation_method_properties = KISAO_METHOD_MAP.get(task.simulation.algorithm.kisao_id, None)

    if simulation_method_properties is None:
        raise NotImplementedError("".join([
            "Algorithm with KiSAO id '{}' is not supported. ".format(task.simulation.algorithm.kisao_id),
            "Algorithm must have one of the following KiSAO ids:\n  - {}".format('\n  - '.join(
                '{}: {}'.format(kisao_id, method_properties['name'])
                for kisao_id, method_properties in KISAO_METHOD_MAP.items())),
        ]))

    simulation_method = simulation_method_properties['method']

    #############################################################
    # Apply the algorithm parameter changes specified by `simulation.algorithm.parameter_changes`
    simulation_args = {}
    for change in task.simulation.algorithm.changes:
        parameter_properties = simulation_method_properties['parameters'].get(change.kisao_id, None)

        if parameter_properties is None:
            raise NotImplementedError("".join([
                "Algorithm parameter with KiSAO id '{}' is not supported. ".format(change.kisao_id),
                "Parameter must have one of the following KiSAO ids:\n  - {}".format('\n  - '.join(
                    '{}: {}'.format(kisao_id, parameter['name'])
                    for kisao_id, parameter in simulation_method_properties['parameters'].items())),
            ]))

        simulation_args[parameter_properties['arg']] = parse_value(change.new_value, parameter_properties['type'])

    #############################################################
    # Configure the simulation. For example, for time course simulations set up the time points to record
    simulation_args['initial_time'] = task.simulation.initial_time
    simulation_args['output_start_time'] = task.simulation.output_start_time
    simulation_args['output_end_time'] = task.simulation.output_end_time
    simulation_args['number_of_points'] = task.simulation.number_of_points

    #############################################################
    # Execute the simulation and record the results
    results = simulation_method(model, **simulation_args)

    #############################################################
    # Transform the results to an instance of :obj:`DataGeneratorVariableResults`
    variable_results = DataGeneratorVariableResults()
    for variable in variables:
        variable_results[variable.id] = get_sed_variables_from_results(results, target_x_paths_ids, variable.id)

    #############################################################
    # log action
    log.algorithm = task.simulation.algorithm.kisao_id
    log.simulator_details = {
        'method': simulation_method.__module__ + '.' + simulation_method.__name__,
        'arguments': simulation_args,
    }

    #############################################################
    # Return the results of the variables and the log
    return variable_results, log
