"""
Copyright (c) 2025 MeteoSwiss, contributors listed in AUTHORS

Distributed under the terms of the BSD 3-Clause License.

SPDX-License-Identifier: BSD-3-Clause

Visualization functions for impact forecasts and warnings.
"""

import geopandas as gpd
import numpy as np

from climada.engine import Impact
from climada.entity import Exposures

from impact_forecasting_warning.visualization import util_functions as u_func


def create_national_plot(impact: Impact, exp_ch: Exposures, reference_time: str, valid_time_print: str,
                         base_str: str) -> None:
    """
    Create and save national impact histogram plot.

    :param impact: Impact object for a specific forecast day.
    :type impact: Impact
    :param exp_ch: Exposure object for Switzerland.
    :type exp_ch: Exposures
    :param reference_time: Reference time string.
    :type reference_time: str
    :param valid_time_print: Valid time string for display.
    :type valid_time_print: str
    :param base_str: Base string for output file path.
    :type base_str: str
    :return: None
    :rtype: None
    """
    shift_bins = max(np.round(np.log10(np.mean(impact.at_event))) - 3, 0)
    bins = np.geomspace(10**shift_bins, 10**(5 + shift_bins), 11)

    ax = u_func.plot_impact_log_hist(
        impact,
        title=f"National impact-based forecast for $\\bf{{{valid_time_print}}}$ (init time: {reference_time})",
        impact_label=f"Total building damages ({exp_ch.value_unit})",
        bins=bins,
        ticks=bins[::2],
        figsize=(6, 4),
    )

    mean_impact = np.mean(impact.at_event)
    ax.text(0.6,
            0.9,
            f"mean damage: {exp_ch.value_unit} {mean_impact:,.0f}".replace(",", "'"),
            transform=ax.transAxes,
            fontdict={"fontsize": 12},
            bbox=dict(boxstyle="round,pad=0.5", facecolor="white", edgecolor="black"))
    ax.get_figure().savefig(base_str + "_histbin.svg", dpi=300, bbox_inches='tight')


def create_cantonal_plot(impact: Impact, exp_ch: Exposures, gdf_cantons: gpd.GeoDataFrame,
                         shift_center_of_mass_by_name: dict, reference_time: str, valid_time_print: str, base_str: str,
                         base_str_output_data: str, forecast_day: int) -> None:
    """
    Create and save cantonal impact piechart map.

    :param impact: Impact object for a specific forecast day.
    :type impact: Impact
    :param exp_ch: Exposure object for Switzerland.
    :type exp_ch: Exposures
    :param gdf_cantons: GeoDataFrame with canton shapes.
    :type gdf_cantons: gpd.GeoDataFrame
    :param shift_center_of_mass_by_name: Dictionary for shifting canton labels.
    :type shift_center_of_mass_by_name: dict
    :param reference_time: Reference time string.
    :type reference_time: str
    :param valid_time_print: Valid time string for display.
    :type valid_time_print: str
    :param base_str: Base string for output file path.
    :type base_str: str
    :param base_str_output_data: Base string for output data file path.
    :type base_str_output_data: str
    :param forecast_day: Day index for the forecast.
    :type forecast_day: int
    :return: None
    :rtype: None
    """
    bins = np.geomspace(0.00005, 0.005, 5)

    ax = u_func.plot_member_piechart_per_region(
        impact,
        gdf_cantons,
        "sum",
        pie_rel_size=0.15,
        bins=bins,
        figsize=(8.5, 5.5),
        title=f"Cantonal impact-based forecast for $\\bf{{{valid_time_print}}}$ (init time: {reference_time})",
        cbar_title="Relative impact",
        exposure_for_normalization=exp_ch,
        shift_center_of_mass_by_name=shift_center_of_mass_by_name,
    )
    ax.set_xticks([])
    ax.set_yticks([])
    ax.get_figure().savefig(base_str + "_canton_impact_map.jpeg", dpi=300, bbox_inches='tight')

    # Save canton median data
    impact_per_canton = u_func.aggregate_impacts_by_gdf(impact, gdf_cantons, "sum")
    median_col_name = f"median_estimated_damage [{exp_ch.value_unit}]"
    impact_per_canton[median_col_name] = np.median(impact_per_canton[range(1 + 21 * forecast_day,
                                                                           22 + 21 * forecast_day)],
                                                   axis=1)
    impact_per_canton.rename(columns={"name": "canton"})[[
        "canton", median_col_name
    ]].set_index("canton").to_csv(f"{base_str_output_data}_canton_medians.csv")


def create_warning_plot(imp_warning: Impact, gdf_warningregions: gpd.GeoDataFrame, reference_time: str,
                        valid_time_print: str, base_str: str) -> None:
    """
    Create and save hazard-based warning map.

    :param imp_warning: Median warning impact for a specific forecast day.
    :type imp_warning: Impact
    :param gdf_warningregions: GeoDataFrame with warning region shapes.
    :type gdf_warningregions: gpd.GeoDataFrame
    :param reference_time: Reference time string.
    :type reference_time: str
    :param valid_time_print: Valid time string for display.
    :type valid_time_print: str
    :param base_str: Base string for output file path.
    :type base_str: str
    :return: None
    :rtype: None
    """
    ax = u_func.plot_impact_polygons(
        imp_warning,
        gdf_warningregions,
        agg_func="median",
        title=f"Hazard-based warning for $\\bf{{{valid_time_print}}}$ (init time: {reference_time})",
        figsize=(8.5, 5.5),
    )
    ax.set_xticks([])
    ax.set_yticks([])
    ax.get_figure().savefig(base_str + "_warn_map.jpeg", dpi=300, bbox_inches='tight')


def create_impact_warning_plots(impact: Impact, gdf_warningregions: gpd.GeoDataFrame, reference_time: str,
                                valid_time_print: str, base_str: str) -> None:
    """
    Create and save impact-based warning maps with different thresholds.

    :param impact: Mean impact for a specific forecast day.
    :type impact: Impact
    :param gdf_warningregions: GeoDataFrame with warning region shapes.
    :type gdf_warningregions: gpd.GeoDataFrame
    :param reference_time: Reference time string.
    :type reference_time: str
    :param valid_time_print: Valid time string for display.
    :type valid_time_print: str
    :param base_str: Base string for output file path.
    :type base_str: str
    :return: None
    :rtype: None
    """
    for impact_warning_thresholds, label in zip(
        [np.array([1e4, 1e5, 1e6, 1e7]), np.array([1e4, 1e5, 1e6, 1e7]) / 10], ["large_thresh", "small_thresh"]):
        impact_warning_labels = ["1: Minimal or no damage"] + [
            f"{k+2}: Damage above {u_func.print_large_amounts(thresh)}"
            for k, thresh in enumerate(impact_warning_thresholds)
        ]

        ax = u_func.plot_impact_polygons(
            impact,
            gdf_warningregions,
            agg_func="sum",
            title=f"Impact-based warning for $\\bf{{{valid_time_print}}}$ (init time: {reference_time})",
            figsize=(8.5, 5.5),
            warning_thresholds=impact_warning_thresholds,
            warning_labels=impact_warning_labels)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.get_figure().savefig(base_str + f"_impact_warn_map_{label}.jpeg", dpi=300, bbox_inches='tight')


def create_relative_impact_warning_plots(impact: Impact, exp_ch: Exposures, gdf_warningregions: gpd.GeoDataFrame,
                                         reference_time: str, valid_time_print: str, base_str: str) -> None:
    """
    Create and save relative-impact-based warning maps.

    :param impact: Mean impact for a specific forecast day.
    :type impact: Impact
    :param exp_ch: Exposure object for Switzerland.
    :type exp_ch: Exposures
    :param gdf_warningregions: GeoDataFrame with warning region shapes.
    :type gdf_warningregions: gpd.GeoDataFrame
    :param reference_time: Reference time string.
    :type reference_time: str
    :param valid_time_print: Valid time string for display.
    :type valid_time_print: str
    :param base_str: Base string for output file path.
    :type base_str: str
    :return: None
    :rtype: None
    """
    for relative_impact_warning_thresholds, label in zip(
        [np.array([1e-5, 1e-4, 1e-3, 1e-2]),
         np.array([1e-5, 1e-4, 1e-3, 1e-2]) / 10], ["large_thresh", "small_thresh"]):
        relative_impact_warning_labels = ["1: Minimal or no damage"] + [
            f"{k+2}: Damage above " + (f"{thresh*100:.3f} %" if label == "large_thresh" else f"{thresh*100:.4f} %")
            for k, thresh in enumerate(relative_impact_warning_thresholds)
        ]

        ax = u_func.plot_impact_polygons(
            impact,
            gdf_warningregions,
            agg_func="sum",
            exposure_for_normalization=exp_ch,
            title=f"Relative-impact-based warning for $\\bf{{{valid_time_print}}}$ (init time: {reference_time})",
            figsize=(8.5, 5.5),
            warning_thresholds=relative_impact_warning_thresholds,
            warning_labels=relative_impact_warning_labels)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.get_figure().savefig(base_str + f"_rel_impact_warn_map_{label}.jpeg", dpi=300, bbox_inches='tight')


def create_impact_map(impact: Impact, exp_ch: Exposures, gdf_warningregions: gpd.GeoDataFrame, reference_time: str,
                      valid_time_print: str, base_str: str) -> None:
    """
    Create and save impact-based forecast map.

    :param impact: Mean impact for a specific forecast day.
    :type impact: Impact
    :param exp_ch: Exposure object for Switzerland.
    :type exp_ch: Exposures
    :param gdf_warningregions: GeoDataFrame with warning region shapes.
    :type gdf_warningregions: gpd.GeoDataFrame
    :param reference_time: Reference time string.
    :type reference_time: str
    :param valid_time_print: Valid time string for display.
    :type valid_time_print: str
    :param base_str: Base string for output file path.
    :type base_str: str
    :return: None
    :rtype: None
    """
    ax = u_func.plot_impact_with_region_shapes(
        impact,
        gdf_warningregions,
        title=f"Impact-based forecast for $\\bf{{{valid_time_print}}}$ (init time: {reference_time})",
        cbar_title=f"Building damages ({exp_ch.value_unit}), mean over forecast members",
        vmin=100,
        vmax=1e5,
    )
    ax.set_xticks([])
    ax.set_yticks([])
    ax.get_figure().savefig(base_str + "_impact_map.jpeg", dpi=300, bbox_inches='tight')
