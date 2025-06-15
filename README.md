EasyData provides a streamlined solution that lets you issue natural language commands to retrieve sensor data from InfluxDB or an MCP server. The OpenAI Swarm framework orchestrates multiple agents to gather and clean the data, and the OpenAI Code Interpreter automatically generates a chart that is saved locally.

## Project Overview

EasyData combines three building blocks:

* **Swarm** coordinates specialized agents responsible for data retrieval, preprocessing, and visualization.
* The **OpenAI Code Interpreter** safely runs Python code and creates diagrams as PNG or SVG without manual postprocessing.
* **InfluxDB** or a compatible MCP server stores real-time time series data and is accessed via the Python client library.

## Goals

* Natural language queries for common sensor types
* Automated chart creation without manual steps
* Dynamic visualization types powered by the OpenAI API
* Extensible multi-agent architecture for additional data sources or output formats

## Architecture

### Data Flow

1. A user issues a query such as "show me the last three hours of the CO2 sensor and temperature sensor".
2. A retrieval agent fetches the corresponding time series from InfluxDB.
3. An analysis agent validates the time window, data type, and unit.
4. The visualization agent generates Python code, which the Code Interpreter executes, saving the chart with `plt.savefig()` and returning the file path.

### Main Components

* **Swarm agents** handle retrieval, validation, and visualization tasks.
* **OpenAI Assistants API** manages thread context and tools.
* **InfluxDB 2.x** is the time-series database using the Flux query language.
* **MCP server** bridges sensor networks that lack direct database access.

## Installation

### Prerequisites

* Python 3.11
* Access token for the OpenAI API
* Running InfluxDB instance or MCP server

### Setup

```bash
git clone https://github.com/your-org/easydata
cd easydata
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt   # includes openai, influxdb_client, matplotlib, pandas, swarm
```
## Configuration

Copy `configs/.env.example` to `.env` and provide the InfluxDB URL, token, organization and bucket name before running EasyData. Set `OPENAI_API_KEY` to enable dynamic chart creation via the OpenAI API.

### Command Line Usage

```
python -m easydata <flux-query> --chart line --title "My Chart" --output plot.png
```

Use the `--prompt` option to supply natural language instructions for dynamic chart creation:

```
python -m easydata <flux-query> --prompt "Create a pie chart of the latest values" --output latest.png
```


## Example Workflow

```example
"""Python script executed by the Code Interpreter
# pip install influxdb_client matplotlib pandas

import pandas as pd
import matplotlib.pyplot as plt
from influxdb_client import InfluxDBClient

token = "INFLUX_TOKEN"
org = "my_org"
bucket = "sensors"
query = '''
from(bucket: "sensors")
  |> range(start: -3h)
  |> filter(fn: (r) => r._measurement == "environment")
  |> filter(fn: (r) => r.sensor == "co2" or r.sensor == "temperature")
'''

with InfluxDBClient(url="https://influx.example.com", token=token, org=org) as client:
    df = client.query_api().query_data_frame(query)

df = df.pivot(index="_time", columns="sensor", values="_value")
df.plot(figsize=(12,5))
plt.title("CO₂ and Temperature over the last three hours")
plt.xlabel("Time")
plt.ylabel("Value")
plt.grid(True)
plt.savefig("easydata_output.png", dpi=300)
"""
```

The interpreter returns `easydata_output.png`, which can be downloaded directly from the chat.

## Security and Privacy

* Queries only contain metadata and are not persisted after the session ends.
* InfluxDB access tokens are kept in memory during the session and discarded when the process exits.
* Sensor data stays in your infrastructure and is used only for read access.

## License

EasyData is licensed under the Apache-2.0 License.
