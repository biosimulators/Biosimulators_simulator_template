""" Methods for executing SED tasks and saving their results

:Author: Author name <email@organization>
:Date: YYYY-MM-DD
:Copyright: YYYY, Owner
:License: <License, e.g., MIT>
"""

from .data_model import KISAO_METHOD_MAP
from biosimulators_utils.combine.exec import exec_sedml_docs_in_archive
from biosimulators_utils.config import get_config, Config  # noqa: F401
from biosimulators_utils.log.data_model import CombineArchiveLog, TaskLog, StandardOutputErrorCapturerLevel  # noqa: F401
from biosimulators_utils.viz.data_model import VizFormat  # noqa: F401
from biosimulators_utils.report.data_model import ReportFormat, VariableResults, SedDocumentResults  # noqa: F401
from biosimulators_utils.sedml import validation
from biosimulators_utils.sedml.data_model import (Task, ModelLanguage, ModelAttributeChange,  # noqa: F401
                                                  UniformTimeCourseSimulation, Variable)
from biosimulators_utils.sedml.exec import exec_sed_doc as base_exec_sed_doc
from biosimulators_utils.simulator.utils import get_algorithm_substitution_policy
from biosimulators_utils.utils.core import parse_value, raise_errors_warnings
from kisao.utils import get_preferred_substitute_algorithm_by_ids
from my_simulator import read_model, get_sed_variables_from_results

__all__ = ['get_simulator_version', 'exec_sedml_docs_in_combine_archive', 'exec_sed_doc', 'exec_sed_task', 'preprocess_sed_task']


def get_simulator_version():
    """ Get the version of MySimulator

    Returns:
        :obj:`str`: version
    """
    return my_simulator.__version__


def exec_sedml_docs_in_combine_archive(archive_filename, out_dir, config=None):
    """ Execute the SED tasks defined in a COMBINE/OMEX archive and save the outputs

    Args:
        archive_filename (:obj:`str`): path to COMBINE/OMEX archive
        out_dir (:obj:`str`): path to store the outputs of the archive

            * CSV: directory in which to save outputs to files
              ``{ out_dir }/{ relative-path-to-SED-ML-file-within-archive }/{ report.id }.csv``
            * HDF5: directory in which to save a single HDF5 file (``{ out_dir }/reports.h5``),
              with reports at keys ``{ relative-path-to-SED-ML-file-within-archive }/{ report.id }`` within the HDF5 file

        config (:obj:`Config`, optional): BioSimulators common configuration

    Returns:
        :obj:`tuple`:

            * :obj:`SedDocumentResults`: results
            * :obj:`CombineArchiveLog`: log
    """
    return exec_sedml_docs_in_archive(exec_sed_doc, archive_filename, out_dir,
                                      apply_xml_model_changes=True,
                                      config=config)


def exec_sed_doc(doc, working_dir, base_out_path, rel_out_path=None,
                 apply_xml_model_changes=False,
                 log=None, indent=0, pretty_print_modified_xml_models=False,
                 log_level=StandardOutputErrorCapturerLevel.c, config=None):
    """ Execute the tasks specified in a SED document and generate the specified outputs

    Args:
        doc (:obj:`SedDocument` or :obj:`str`): SED document or a path to SED-ML file which defines a SED document
        working_dir (:obj:`str`): working directory of the SED document (path relative to which models are located)

        base_out_path (:obj:`str`): path to store the outputs

            * CSV: directory in which to save outputs to files
              ``{base_out_path}/{rel_out_path}/{report.id}.csv``
            * HDF5: directory in which to save a single HDF5 file (``{base_out_path}/reports.h5``),
              with reports at keys ``{rel_out_path}/{report.id}`` within the HDF5 file

        rel_out_path (:obj:`str`, optional): path relative to :obj:`base_out_path` to store the outputs
        apply_xml_model_changes (:obj:`bool`, optional): if :obj:`True`, apply any model changes specified in the SED-ML file before
            calling :obj:`task_executer`.
        log (:obj:`SedDocumentLog`, optional): log of the document
        indent (:obj:`int`, optional): degree to indent status messages
        pretty_print_modified_xml_models (:obj:`bool`, optional): if :obj:`True`, pretty print modified XML models
        log_level (:obj:`StandardOutputErrorCapturerLevel`, optional): level at which to log output
        config (:obj:`Config`, optional): BioSimulators common configuration
        simulator_config (:obj:`SimulatorConfig`, optional): tellurium configuration

    Returns:
        :obj:`tuple`:

            * :obj:`ReportResults`: results of each report
            * :obj:`SedDocumentLog`: log of the document
    """
    return base_exec_sed_doc(exec_sed_task, doc, working_dir, base_out_path,
                             rel_out_path=rel_out_path,
                             apply_xml_model_changes=apply_xml_model_changes,
                             log=log,
                             indent=indent,
                             pretty_print_modified_xml_models=pretty_print_modified_xml_models,
                             log_level=log_level,
                             config=config)


def exec_sed_task(task, variables, preprocessed_task=None, log=None, config=None):
    ''' Execute a task and save its results

    Args:
        task (:obj:`Task`): task
        variables (:obj:`list` of :obj:`Variable`): variables that should be recorded
        preprocessed_task (:obj:`object`, optional): preprocessed information about the task, including possible
            model changes and variables. This can be used to avoid repeatedly executing the same initialization
            for repeated calls to this method.
        log (:obj:`TaskLog`, optional): log for the task
        config (:obj:`Config`, optional): BioSimulators common configuration

    Returns:
        :obj:`tuple`:

            :obj:`VariableResults`: results of variables
            :obj:`TaskLog`: log

    Raises:
        :obj:`ValueError`: if the task or an aspect of the task is not valid, or the requested output variables
            could not be recorded
        :obj:`NotImplementedError`: if the task is not of a supported type or involves an unsuported feature
    '''
    config = config or get_config()
    if config.LOG and not log:
        log = TaskLog()

    if preprocessed_task is None:
        preprocessed_task = preprocess_sed_task(task, variables, config=config)

    #############################################################
    model = task.model
    sim = task.simulation

    if config.VALIDATE_SEDML:
        # Validate task
        raise_errors_warnings(validation.validate_task(task),
                              error_summary='Task `{}` is invalid.'.format(task.id))

        # Validate that the model is encoded in a supported language
        raise_errors_warnings(validation.validate_model_language(model.language, ModelLanguage.SBML),
                              error_summary='Language for model `{}` is not supported.'.format(model.id))

        # Validate that the model changes are of the supported types
        raise_errors_warnings(validation.validate_model_change_types(model.changes, ()),
                              error_summary='Changes for model `{}` are not supported.'.format(model.id))

        # Validate model changes
        raise_errors_warnings(*validation.validate_model_changes(task.model),
                              error_summary='Changes for model `{}` are invalid.'.format(model.id))

        # Validate that the simulation is a supported type of simulation
        raise_errors_warnings(validation.validate_simulation_type(sim, (UniformTimeCourseSimulation, )),
                              error_summary='{} `{}` is not supported.'.format(sim.__class__.__name__, sim.id))

        # Validate time course settings
        raise_errors_warnings(*validation.validate_simulation(sim),
                              error_summary='Simulation `{}` is invalid.'.format(sim.id))

        # Validate that variables of data generators have valid symbols and targets
        raise_errors_warnings(*validation.validate_data_generator_variables(variables),
                              error_summary='Data generator variables for task `{}` are invalid.'.format(task.id))

    # If the model is encoded in XML, check that the XPaths for the variables are valid
    target_x_paths_ids = validation.validate_target_xpaths(variables, model.source, attr='id')

    # Check that the simulation tool can produce each variables -- the simulation tool supports each symbol and target

    #############################################################
    # Read the model located at `task.model.source`; `exec_sedml_docs_in_archive` has already resolved the model and
    # applied any changes
    model = read_model(task.model.source, language=task.model.language)

    #############################################################
    # Load the algorithm specified by `simulation.algorithm`
    alg_kisao_id = get_preferred_substitute_algorithm_by_ids(
        simulation.algorithm.kisao_id, KISAO_METHOD_MAP.keys(),
        substitution_policy=get_algorithm_substitution_policy(config=config))
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
    if config.LOG:
        log.algorithm = alg_kisao_id
        log.simulator_details = {
            'method': simulation_method.__module__ + '.' + simulation_method.__name__,
            'arguments': simulation_args,
        }

    #############################################################
    # Return the results of the variables and the log
    return variable_results, log


def preprocess_sed_task(task, variables, config=None):
    """ Preprocess a SED task, including its possible model changes and variables. This is useful for avoiding
    repeatedly initializing tasks on repeated calls of :obj:`exec_sed_task`.

    Args:
        task (:obj:`Task`): task
        variables (:obj:`list` of :obj:`Variable`): variables that should be recorded
        config (:obj:`Config`, optional): BioSimulators common configuration

    Returns:
        :obj:`object`: preprocessed information about the task
    """
    pass
