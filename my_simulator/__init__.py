import my_simulator

from ._version import __version__  # noqa: F401
# :obj:`str`: version

from .core import exec_sed_task, exec_sedml_docs_in_combine_archive  # noqa: F401

__all__ = [
    '__version__',
    'get_simulator_version',
    'exec_sed_task',
    'exec_sedml_docs_in_combine_archive',
]


def get_simulator_version():
    """ Get the version of MySimulator

    Returns:
        :obj:`str`: version
    """
    return my_simulator.__version__
