"""
Copyright (c) 2025 MeteoSwiss, contributors listed in AUTHORS

Distributed under the terms of the BSD 3-Clause License.

SPDX-License-Identifier: BSD-3-Clause

Exposure creation and preparation functions.
"""

import srtm

from climada.entity import Exposures
from climada.hazard.forecast import HazardForecast


def prepare_elevation_based_exposure(haz_fc: HazardForecast, elevation_threshold: float = 1600.0) -> Exposures:
    """
    Prepare exposure with elevation-based warning thresholds.
    
    Creates a constant-value exposure for all centroids in Switzerland, with different
    impact function assignments based on elevation (for elevation-dependent warning levels).

    :param haz_fc: HazardForecast object.
    :type haz_fc: HazardForecast
    :param elevation_threshold: Elevation threshold in meters for different warning levels.
    :type elevation_threshold: float
    :return: Exposure object with elevation-based impact function assignments.
    :rtype: Exposures
    """
    haz_fc.centroids.set_region_id()
    constant_exposure_gdf = haz_fc.centroids.gdf

    # Filter for Switzerland only (ISO numeric code 756)
    constant_exposure_gdf = constant_exposure_gdf.loc[constant_exposure_gdf["region_id"] == 756]
    constant_exposure_gdf.drop(columns="on_land", inplace=True)
    constant_exposure_gdf["value"] = 1.0
    constant_exposure_gdf["impf_"] = 1

    # Get elevation data for each centroid
    elev = srtm.get_data()
    constant_exposure_gdf["elevation"] = [
        elev.get_elevation(lat, lon)
        for lon, lat in zip(constant_exposure_gdf.geometry.x, constant_exposure_gdf.geometry.y)
    ]

    constant_exposure = Exposures(constant_exposure_gdf)

    # Locations above elevation threshold have different warning thresholds
    constant_exposure.data.loc[constant_exposure_gdf["elevation"] > elevation_threshold, "impf_"] = 2
    constant_exposure.assign_centroids(haz_fc, threshold=100)

    return constant_exposure
