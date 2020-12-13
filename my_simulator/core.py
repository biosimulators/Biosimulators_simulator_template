""" Methods for executing SED tasks and saving their results

:Author: Author name <email@organization>
:Date: YYYY-MM-DD
:Copyright: YYYY, Owner
:License: <License, e.g., MIT>
"""

from biosimulators_utils.combine.exec import exec_sedml_docs_in_archive
from biosimulators_utils.plot.data_model import PlotFormat  # noqa: F401
from biosimulators_utils.report.data_model import ReportFormat, DataGeneratorVariableResults  # noqa: F401
from biosimulators_utils.sedml.data_model import Task, DataGeneratorVariable  # noqa: F401


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
    """
    exec_sedml_docs_in_archive(archive_filename, exec_sed_task, out_dir,
                               apply_xml_model_changes=True,
                               report_formats=report_formats,
                               plot_formats=plot_formats,
                               bundle_outputs=bundle_outputs,
                               keep_individual_outputs=keep_individual_outputs)


def exec_sed_task(model_filename, model_sed_urn, simulation, working_dir, out_filename, out_format):
    ''' Execute a task and save its results

    Args:
       task (:obj:`Task`): task
       variables (:obj:`list` of :obj:`DataGeneratorVariable`): variables that should be recorded

    Returns:
        :obj:`DataGeneratorVariableResults`: results of variables

    Raises:
        :obj:`ValueError`: if the task or an aspect of the task is not valid, or the requested output variables
            could not be recorded
        :obj:`NotImplementedError`: if the task is not of a supported type or involves an unsuported feature
    '''
    # Validate the task. See utilities in :obj:`biosimulators_utils.sedml.validation`.

    # Read the model located at `task.model.source`

    # Apply the model changes specified by `task.model.changes`

    # Load the algorithm specified by `simulation.algorithm`

    # Apply the algorithm parameter changes specified by `simulation.algorithm.parameter_changes`

    # Configure the simulation e.g., for time course simulations set the time points to record

    # Execute the simulation and record the results

    # transform the results to an instance of :obj:`DataGeneratorVariableResults`

    # return results
    pass
