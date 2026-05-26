"""
Copyright (c) 2025 MeteoSwiss, contributors listed in AUTHORS

Distributed under the terms of the BSD 3-Clause License.

SPDX-License-Identifier: BSD-3-Clause

Weather API client for fetching forecast data from OGD.
"""

import numpy as np
import xarray as xr
from earthkit.data import config
from meteodatalab import ogd_api

# Configure cache policy
config.set("cache-policy", "temporary")


def fetch_ogd_forecast(model: str = "ogd-forecasting-icon-ch2",
                       variable: str = "VMAX_10M",
                       reftime: str = "latest",
                       n_days: int = 5) -> xr.DataArray:
    """
    Fetch weather forecast data from OGD API.

    :param model: Model name for OGD API.
    :type model: str
    :param variable: NWP variable name (e.g., "VMAX_10M" for wind, "TOT_PREC" for precipitation).
    :type variable: str
    :param reftime: Reference datetime for the forecast.
    :type reftime: str
    :param n_days: Number of forecast days to retrieve.
    :type n_days: int
    :return: DataArray containing forecast data for all ensemble members.
    :rtype: xr.DataArray
    """
    lead_times = [f"P0DT{i}H" for i in np.arange(0, n_days * 24)]

    # Request deterministic forecast
    req_det = ogd_api.Request(
        collection=model,
        variable=variable,
        reference_datetime=reftime,
        perturbed=False,
        lead_time=lead_times,
    )
    forecast_det = ogd_api.get_from_ogd(req_det)

    # Request perturbed forecasts
    req_pert = ogd_api.Request(
        collection=model,
        variable=variable,
        reference_datetime=reftime,
        perturbed=True,
        lead_time=lead_times,
    )
    forecast_pert = ogd_api.get_from_ogd(req_pert)

    # Concatenate deterministic and perturbed forecasts
    da_forecast = xr.concat([forecast_det, forecast_pert], dim="eps")

    return da_forecast
