# Codex Agent Instructions for EasyData

This repository implements **EasyData**, an automation tool that uses natural language instructions to query sensor data from InfluxDB and visualize it with the OpenAI Code Interpreter orchestrated by the Swarm framework.

## Coding guidelines

- All code, comments and documentation must be written in **English**.
- Python 3.11 is the target runtime. Use type hints where possible.
- Organize source files inside the `src/` directory and tests inside `tests/`.
- Commit messages and branch names are written in English.

## Architecture overview

- **Swarm**: Coordinates specialized agents (data retrieval, preprocessing and visualization).
- **OpenAI Assistants API**: Executes Python code via the Code Interpreter to generate plots.
- **InfluxDB 2.x**: Stores time-series sensor data, queried through the `influxdb_client` package.
- **Output**: Charts are saved locally as PNG or SVG.

## Folder structure (recommended)

```
src/        Python modules for the agents and utilities
src/cli/    Command line interface entry point
tests/      Unit and integration tests
configs/    Configuration files (e.g. example environment variables)
```

## Setup

Create a virtual environment and install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Testing

When tests are available, run them using:

```bash
pytest
```

Linting can be done with `flake8`.

## PR guidelines

Pull requests should include a summary of the changes and a section describing the test results. If tests cannot be executed due to missing dependencies or network restrictions, mention it explicitly.

