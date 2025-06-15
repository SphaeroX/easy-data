from __future__ import annotations

from influxdb_client import InfluxDBClient
import pandas as pd

from .config import InfluxConfig


class DataRetriever:
    """Fetches sensor data from InfluxDB using Flux queries."""

    def __init__(self, config: InfluxConfig) -> None:
        self.config = config

    def query(self, flux_query: str) -> pd.DataFrame:
        """Execute a Flux query and return the results as a DataFrame."""
        with InfluxDBClient(url=self.config.url, token=self.config.token, org=self.config.org) as client:
            data_frame = client.query_api().query_data_frame(flux_query)
        return data_frame
