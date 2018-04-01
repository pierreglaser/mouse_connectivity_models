"""
Module containing Experiment object and supporting functions
"""

# Authors: Joseph Knox josephk@alleninstitute.org
# License:
from __future__ import division

import numpy as np


def compute_centroid(injection_density):
    """Computes centroid in index coordinates.

    Parameters
    ----------
    injection_density : array, shape (x_ccf, y_ccf, z_ccf)
        injection_density data volume.

    Returns
    -------
        centroid onf injection_density in index coordinates.

    """
    nonzero = injection_density[injection_density.nonzero()]
    voxels = np.argwhere(injection_density)

    return np.dot(nonzero, voxels) / injection_density.sum()


def get_injection_hemisphere_id(injection_density, majority=False):
    """Gets injection hemisphere based on injection density.

    Defines injection hemisphere by the ratio of the total injection_density
    in each hemisphere.

    Parameters
    ----------
    injection_density : array, shape (x_ccf, y_ccf, z_ccf)
        injection_density data volume.

    Returns
    -------
    int
        injection_hemisphere
    """
    if len(injection_density.shape) != 3:
        raise ValueError("injection_density must be 3-array")

    # split along depth dimension (forces arr.shape[2] % 2 == 0)
    hemis = np.dsplit(injection_density, 2)
    hemi_sums = tuple(map(np.sum, hemis))

    # if not looking for either l or r
    if not majority and all(hemi_sums):
        return 3

    left_sum, right_sum = hemi_sums
    if left_sum > right_sum:
        return 1

    return 2