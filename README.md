# confident-mcp

Confident AI's open-source Model Context Protocol (MCP) Server.

## ⚠️ Important Warning: Public Endpoint

Please note that the hosted `/mcp` endpoint is strictly for internal development and experimental use. **It is not designed for public consumption.** The API and its underlying data structures are unstable and **subject to change, breaking updates, or removal at any time without prior notice.** Do not build production applications or rely on this public endpoint for any critical workflows. 


## Installation

This project uses [Poetry](https://python-poetry.org/) for dependency management. To install the project and its dependencies, run:

```bash
poetry install
```

## Usage

```bash
uv run src/server.py
```