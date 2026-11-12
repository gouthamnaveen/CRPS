import unittest

import numpy as np

from CRPS.CRPS import CRPS


class MissingValueTests(unittest.TestCase):
    def test_nan_observations(self):
        observations = (np.nan, float('nan'), np.float32('nan'),
                        np.float64('nan'), np.array([np.nan])[0])
        for observation in observations:
            with self.subTest(observation_type=type(observation)):
                scores = CRPS(np.array([1.0, 2.0, 3.0]), observation).compute()
                self.assertTrue(np.isnan(scores).all(), scores)

    def test_nan_ensemble_member(self):
        scores = CRPS(np.array([1.0, np.nan, 3.0]), 2.0).compute()
        self.assertTrue(np.isnan(scores).all())

    def test_finite_observations(self):
        ensemble = np.array([1.0, 2.0, 3.0])
        for observation in (0.0, 1.0, 1.5, 2.0, 3.0, 4.0):
            with self.subTest(observation=observation):
                # Independent pairwise-distance formula for empirical CRPS.
                expected = np.abs(ensemble - observation).mean()
                expected -= np.abs(ensemble[:, None] - ensemble).mean() / 2
                crps, fair, adjusted = CRPS(ensemble, observation).compute()
                self.assertAlmostEqual(crps, expected)
                self.assertAlmostEqual(fair, expected - 2 / 9)
                self.assertAlmostEqual(adjusted, expected - (1 - 3 / 200) * 2 / 9)


if __name__ == '__main__':
    unittest.main()
