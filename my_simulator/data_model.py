""" Data model for the mapping between KISAO terms and simulation methods and their arguments

:Author: Author name <email@organization>
:Date: YYYY-MM-DD
:Copyright: YYYY, Owner
:License: <License, e.g., MIT>
"""

from biosimulators_utils.data_model import ValueType
import collections
import my_simulator

__all__ = ['KISAO_METHOD_MAP']

KISAO_METHOD_MAP = collections.OrderedDict([
    ('KISAO_XXXXXXXX', {
        'name': 'simulation method',
        'method': my_simulator.simulation_method,
        'parameters': {
            'KISAO_XXXXXXXX': {
                'name': {
                    'argument_name': 'rtol',
                    'type': ValueType.float,
                    'default': 1e-8,
                }
            },
        }
    })
])
