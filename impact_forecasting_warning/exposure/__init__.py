"""
Copyright (c) 2025 MeteoSwiss, contributors listed in AUTHORS

Distributed under the terms of the BSD 3-Clause License.

SPDX-License-Identifier: BSD-3-Clause

Exposure module: Exposure data loading and creation.
"""

from impact_forecasting_warning.exposure.exposure_data import create_litpop_exposure, load_geodataframes
from impact_forecasting_warning.exposure.exposure_creation import prepare_elevation_based_exposure

__all__ = [
    "create_litpop_exposure",
    "load_geodataframes",
    "prepare_elevation_based_exposure",
]
