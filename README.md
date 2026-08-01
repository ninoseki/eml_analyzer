# EML analyzer

[![Coverage Status](https://coveralls.io/repos/github/ninoseki/eml_analyzer/badge.svg?branch=master)](https://coveralls.io/github/ninoseki/eml_analyzer?branch=master)

EML analyzer is an application to analyze the EML file which can:

- Analyze headers.
- Analyze bodies.
  - Extract IOCs (URLs, domains, IP addresses, emails) in bodies.
- Analyze attachments.
  - Identify whether attachments contain suspicious OLE files.

## Installation

### Docker

Container images are available via GHCR: https://github.com/ninoseki/eml_analyzer/pkgs/container/eml_analyzer.

- `latest`: the latest version with spamd
- `latest-slim`: the latest slim version (without spamd)

## Configuration

Configuration can be done via environment variables.

Alternatively you can set values through `.env` file. Values in `.env` file will be automatically loaded.

| Key                          | Desc.                                           | Default     |
| ---------------------------- | ----------------------------------------------- | ----------- |
| `REDIS_EXPIRE`               | Redis cache expiration time (in seconds)        | 3600        |
| `REDIS_KEY_PREFIX`           | Redis key prefix                                | `analysis`  |
| `REDIS_URL`                  | Redis URL                                       | -           |
| `REDIS_CACHE_LIST_AVAILABLE` | Expose a list of cached keys                    | True        |
| `SPAMASSASSIN_HOST`          | SpamAssassin host                               | `127.0.0.1` |
| `SPAMASSASSIN_PORT`          | SpamAssassin port                               | 783         |
| `SPAMASSASSIN_TIMEOUT`       | SpamAssassin timeout (in seconds)               | 10          |
| `URLSCAN_API_KEY`            | urlscan.io API Key                              | -           |
| `VIRUSTOTAL_API_KEY`         | VirusTotal API Key                              | -           |
| `ASYNC_MAX_AT_ONCE`          | Max number of concurrently running lookup tasks | `None`      |
| `ASYNC_MAX_PER_SECOND`       | Max number of tasks spawned per second          | `None`      |

## Development

### Requirements

- Python 3.14
- Node.js v24
- Docker & Docker Compose
- Lefthook

### Backend

```bash
# install dependencies
uv sync
# run test
uv run pytest
```

### Frontend

```bash
cd frontend
# install dependencies
npm install
# run test
npm run test:unit
```

### Linter

```bash
# setup pre-commit hooks
lefthook install
# run hooks manually
lefthook run pre-commit --all-files
```

## ToDo

- [x] Support MSG format.
- [ ] In-depth attachments analysis by using oletools.
