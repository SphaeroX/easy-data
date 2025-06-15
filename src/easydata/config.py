from dataclasses import dataclass
import os


@dataclass
class InfluxConfig:
    url: str
    token: str
    org: str
    bucket: str


def load_influx_config() -> InfluxConfig:
    """Load InfluxDB configuration from environment variables."""
    url = os.environ.get("INFLUXDB_URL")
    token = os.environ.get("INFLUXDB_TOKEN")
    org = os.environ.get("INFLUXDB_ORG")
    bucket = os.environ.get("INFLUXDB_BUCKET")

    if not all([url, token, org, bucket]):
        missing = [name for name in ["INFLUXDB_URL", "INFLUXDB_TOKEN", "INFLUXDB_ORG", "INFLUXDB_BUCKET"] if name not in os.environ]
        raise RuntimeError(f"Missing environment variables: {', '.join(missing)}")

    return InfluxConfig(url=url, token=token, org=org, bucket=bucket)


def load_openai_api_key() -> str:
    """Return the OpenAI API key from the environment."""

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("Missing environment variable: OPENAI_API_KEY")
    return api_key
