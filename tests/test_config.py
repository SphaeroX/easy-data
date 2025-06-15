import sys
import pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "src"))

from easydata.config import load_influx_config


def test_load_influx_config(monkeypatch):
    monkeypatch.setenv("INFLUXDB_URL", "http://localhost")
    monkeypatch.setenv("INFLUXDB_TOKEN", "token")
    monkeypatch.setenv("INFLUXDB_ORG", "org")
    monkeypatch.setenv("INFLUXDB_BUCKET", "bucket")

    config = load_influx_config()

    assert config.url == "http://localhost"
    assert config.token == "token"
    assert config.org == "org"
    assert config.bucket == "bucket"
