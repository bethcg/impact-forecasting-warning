"""
Copyright (c) 2025 MeteoSwiss, contributors listed in AUTHORS

Distributed under the terms of the BSD 3-Clause License.

SPDX-License-Identifier: BSD-3-Clause

Pipelines module: Pipeline orchestration and CLI entry points.
"""

from impact_forecasting_warning.pipelines.wind_impact_forecast import run_pipeline

__all__ = [
    "run_pipeline",
]
