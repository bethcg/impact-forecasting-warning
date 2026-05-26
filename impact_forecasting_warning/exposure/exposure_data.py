"""
Copyright (c) 2025 MeteoSwiss, contributors listed in AUTHORS

Distributed under the terms of the BSD 3-Clause License.

SPDX-License-Identifier: BSD-3-Clause

Exposure data loading: LitPop creation, geodata, and elevation data.
"""

import cartopy.crs as ccrs
import geopandas as gpd
import numpy as np

from climada import CONFIG
from climada.entity import LitPop

# Define data paths
PATH_TO_WARNINGREGION_SHAPES = f"{CONFIG.local_data.data_dir}/warning_regions/Warningregions.shp"
PATH_TO_CANTON_SHAPES = f"{CONFIG.local_data.data_dir}/ch_shapefile/swissTLMRegio_KANTONSGEBIET_LV95.shp"


def create_litpop_exposure(convert_to_chf: bool = True) -> LitPop:
    """
    Create LitPop exposure for Switzerland.

    :param convert_to_chf: If True, convert exposure values from USD to CHF (factor 0.78).
    :type convert_to_chf: bool
    :return: LitPop exposure object for Switzerland.
    :rtype: LitPop
    """
    exp_ch = LitPop.from_countries("CHE")

    if convert_to_chf:
        # Convert to CHF
        exp_ch.data["value"] = 0.78 * exp_ch.data["value"]
        exp_ch.value_unit = "CHF"

    return exp_ch


def load_geodataframes() -> tuple:
    """
    Load and prepare GeoDataFrames for warning regions and cantons.

    :return: Tuple containing (warning_regions_gdf, cantons_gdf, shift_center_of_mass_by_name).
    :rtype: tuple
    """
    # Prepare warning region shapes
    gdf_warningregions = gpd.read_file(PATH_TO_WARNINGREGION_SHAPES)
    gdf_warningregions.crs = ccrs.epsg(21781)
    gdf_warningregions = gdf_warningregions.dissolve(by="REGION_NAM", as_index=False)
    gdf_warningregions = gdf_warningregions[["REGION_NAM", "geometry"]]
    gdf_warningregions = gdf_warningregions.to_crs(epsg=4326)

    # Prepare canton shapes
    gdf_cantons = gpd.read_file(PATH_TO_CANTON_SHAPES)
    gdf_cantons = gdf_cantons.to_crs(epsg=4326)
    gdf_cantons = gdf_cantons.dissolve(by="NAME", as_index=False)
    gdf_cantons = gdf_cantons.loc[gdf_cantons.ICC == "CH", :].reset_index(drop=True)
    gdf_cantons = gdf_cantons[["NAME", "geometry"]]

    # Dictionary for shifting canton labels on maps
    shift_center_of_mass_by_name = {
        "Basel-Landschaft": np.array([0.05, 0]),
        "Obwalden": np.array([-0.02, 0]),
        "Nidwalden": np.array([0, 0.01]),
        "St. Gallen": np.array([-0.15, -0.001]),
        "Appenzell Ausserrhoden": np.array([-0.02, 0.05]),
        "Appenzell Innerrhoden": np.array([0.03, -0.04]),
    }

    return gdf_warningregions, gdf_cantons, shift_center_of_mass_by_name
