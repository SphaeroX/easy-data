EasyData bietet eine durchgehende Lösung, mit der Sie natürliche Sprachbefehle verwenden, um Sensordaten aus InfluxDB oder einem MCP Server auszulesen, diese mithilfe des OpenAI-Frameworks Swarm orchestrieren und anschließend durch den OpenAI Code Interpreter automatisiert als Bilddatei visualisieren lassen([github.com][1], [platform.openai.com][2], [docs.influxdata.com][3], [github.com][4], [akira.ai][5], [stackoverflow.com][6], [datacamp.com][7], [github.com][8], [medium.com][9], [community.openai.com][10]).

## Projektüberblick

EasyData verbindet drei Bausteine:

* Swarm koordiniert mehrere spezialisierte Agenten, die jeweils Datenabruf, Datenaufbereitung und Visualisierung übernehmen([akira.ai][5], [github.com][11], [community.openai.com][10]).
* Der Code Interpreter der OpenAI-Plattform führt Python-Code sicher aus und erstellt Diagramme als PNG oder SVG, die ohne weitere Nachbearbeitung heruntergeladen werden können([platform.openai.com][2], [datacamp.com][7]).
* InfluxDB oder ein kompatibler MCP Server stellt Echtzeit-Zeitreihendaten bereit und erlaubt über die Python-Clientbibliothek einen performanten Zugriff([docs.influxdata.com][3], [influxdata.com][12], [github.com][4], [influxdb-python.readthedocs.io][13]).

## Zielsetzung

* Sprachgesteuerte Abfragen für alle gängigen Sensortypen
* Automatisierte Diagrammerstellung ohne manuelle Zwischenschritte
* Erweiterbare Multi Agent-Architektur für weitere Datenquellen oder Ausgabeformate

## Architektur

### Datenfluss

1. Der Nutzer formuliert eine Abfrage wie „zeige mir die letzten drei Stunden den CO2 Sensor und Temperatursensor im Vergleich“.
2. Ein Retrieval-Agent ruft die gewünschten Messreihen aus InfluxDB ab.
3. Ein Analyse-Agent prüft Zeitfenster, Datentyp und Einheit.
4. Der Visualisierungs-Agent erzeugt Python-Code, den der Code Interpreter ausführt, speichert das Diagramm mittels `plt.savefig()` und gibt den Dateilink zurück([stackoverflow.com][6], [geeksforgeeks.org][14]).

### Hauptkomponenten

* **Swarm Agents**: jeweils zuständig für Datenabruf, Validierung, Visualisierung.
* **OpenAI Assistants API**: verwaltet Thread-Kontext und Werkzeuge.
* **InfluxDB 2.x**: Time-Series Datenbank mit Flux Query-Sprache.
* **MCP Server**: Brücke für Sensornetzwerke ohne direkte Datenbankanbindung([github.com][4], [medium.com][9]).

## Installation

### Voraussetzungen

* Python 3.11
* Zugriffsschlüssel für die OpenAI-API
* Laufende InfluxDB Instanz oder MCP Server

### Setup

```bash
git clone https://github.com/your-org/easydata
cd easydata
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt   # enthält openai, influxdb_client, matplotlib, pandas
```

## Beispielworkflow

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

Der Interpreter liefert nach Ausführung die Datei `easydata_output.png`, die direkt im Chat heruntergeladen werden kann.

## Sicherheit und Datenschutz

* Abfragen enthalten nur Metadaten und werden nach Abschluss der Session nicht persistiert.
* Zugriffstoken für InfluxDB werden im Speicher der Session gehalten und nach Beenden des Prozesses verworfen.
* Sensordaten bleiben in der eigenen Infrastruktur und werden nur für Lesezugriffe verwendet.


## Lizenz

EasyData steht unter der Apache-2.0-Lizenz.
