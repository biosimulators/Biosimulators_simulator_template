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
from biosimulators_utils.report.data_model import ReportFormat, VariableResults  # noqa: F401
from biosimulators_utils.sedml import validation
from biosimulators_utils.sedml.data_model import (Task, ModelLanguage, ModelAttributeChange,  # noqa: F401
                                                  UniformTimeCourseSimulation, Variable)
from biosimulators_utils.sedml.exec import exec_sed_doc
from biosimulators_utils.simulator.utils import get_algorithm_substitution_policy
from biosimulators_utils.utils.core import parse_value, raise_errors_warnings
from kisao.utils import get_preferred_substitute_algorithm_by_ids
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
       variables (:obj:`list` of :obj:`Variable`): variables that should be recorded
       log (:obj:`TaskLog`, optional): log for the task

    Returns:
        :obj:`tuple`:

            :obj:`VariableResults`: results of variables
            :obj:`TaskLog`: log

    Raises:
        :obj:`ValueError`: if the task or an aspect of the task is not valid, or the requested output variables
            could not be recorded
        :obj:`NotImplementedError`: if the task is not of a supported type or involves an unsuported feature
    '''
    log = log or TaskLog()

    #############################################################
    model = task.model
    sim = task.simulation

    # Validate that the model is encoded in a supported language
    raise_errors_warnings(validation.validate_model_language(task.model.language, ModelLanguage.SBML),
                          error_summary='Task `{}` is invalid.'.format(task.id))

    # Validate that the model changes are of the supported types
    raise_errors_warnings(validation.validate_model_change_types(task.model.changes, ()),
                          error_summary='Changes for model `{}` are not supported.'.format(model.id))

    # Validate that the simulation is a supported type of simulation
    raise_errors_warnings(validation.validate_simulation_type(task.simulation, (UniformTimeCourseSimulation, )),
                          error_summary='{} `{}` is not supported.'.format(sim.__class__.__name__, sim.id))

    # If the model is encoded in XML, check that the XPaths for the variables are valid
    target_x_paths_ids = validation.validate_variable_xpaths(variables, task.model.source, attr='id')

    # Check that the simulation tool can produce each variables -- the simulation tool supports each symbol and target

    #############################################################
    # Read the model located at `task.model.source`; `exec_sedml_docs_in_archive` has already resolved the model and
    # applied any changes
    model = read_model(task.model.source, language=task.model.language)

    #############################################################
    # Load the algorithm specified by `simulation.algorithm`
    alg_kisao_id = get_preferred_substitute_algorithm_by_ids(
        simulation.algorithm.kisao_id, KISAO_METHOD_MAP.keys(),
        substitution_policy=get_algorithm_substitution_policy())
    simulation_method_properties = KISAO_METHOD_MAP[exec_kisao_id]
    simulation_method = simulation_method_properties['method']

    #############################################################
    # Apply the algorithm parameter changes specified by `simulation.algorithm.parameter_changes`
    simulation_args = {}
    if alg_kisao_id == simulation.algorithm.kisao_id:
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
    # Transform the results to an instance of :obj:`VariableResults`
    variable_results = VariableResults()
    for variable in variables:
        variable_results[variable.id] = get_sed_variables_from_results(results, target_x_paths_ids, variable.id)

    #############################################################
    # log action
    log.algorithm = alg_kisao_id
    log.simulator_details = {
        'method': simulation_method.__module__ + '.' + simulation_method.__name__,
        'arguments': simulation_args,
    }

    #############################################################
    # Return the results of the variables and the log
    return variable_results, log
