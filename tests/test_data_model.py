""" Tests of the data model

:Author: Author name <email@organization>
:Date: YYYY-MM-DD
:Copyright: YYYY, Owner
:License: <License, e.g., MIT>
"""

from my_simulator.data_model import KISAO_METHODS_MAP
import json
import os
import unittest


class DataModelTestCase(unittest.TestCase):
    def test_data_model_matches_specifications(self):
        spec_filename = os.path.join(os.path.dirname(__file__), '..', 'biosimulators.json')
        with open(spec_filename, 'r') as file:
            specs = json.load(file)

        self.assertEqual(
            set(KISAO_METHODS_MAP.keys()),
            set(alg_specs['kisaoId']['id'] for alg_specs in specs['algorithms']))

        for alg_specs in specs['algorithms']:
            alg_props = KISAO_METHODS_MAP[alg_specs['kisaoId']['id']]

            self.assertEqual(set(alg_props['parameters'].keys()), set(param_specs['kisaoId']['id']
                                                                      for param_specs in alg_specs['parameters']))

            for param_specs in alg_specs['parameters']:
                param_props = alg_props['parameters'][param_specs['kisaoId']['id']]

                self.assertEqual(param_props['type'], param_specs['type'])
