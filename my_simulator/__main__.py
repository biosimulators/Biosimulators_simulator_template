""" BioSimulators-compliant command-line interface to the `MySimulator <https://url.for.my.simulator>`_ simulation program.

:Author: Author name <email@organization>
:Date: YYYY-MM-DD
:Copyright: YYYY, Owner
:License: <License, e.g., MIT>
"""

from ._version import __version__
from .core import exec_sedml_docs_in_combine_archive
from biosimulators_utils.simulator.cli import build_cli
import my_simulator

App = build_cli('my-simulator', __version__,
                'My Simulator', my_simulator.__version__, 'https://url.for.my.simulator',
                exec_sedml_docs_in_combine_archive)


def main():
    with App() as app:
        app.run()
