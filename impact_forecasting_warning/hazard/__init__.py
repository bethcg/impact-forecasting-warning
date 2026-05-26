"""
Copyright (c) 2025 MeteoSwiss, contributors listed in AUTHORS

Distributed under the terms of the BSD 3-Clause License.

SPDX-License-Identifier: BSD-3-Clause

Hazard module: Weather data fetching and HazardForecast creation.
"""

from impact_forecasting_warning.hazard.weather_api import fetch_ogd_forecast
from impact_forecasting_warning.hazard.hazard_forecast import create_hazard_forecast

__all__ = [
    "fetch_ogd_forecast",
    "create_hazard_forecast",
]
