# EML analyzer

[![Build Status](https://travis-ci.com/ninoseki/eml_analyzer.svg?branch=master)](https://travis-ci.com/ninoseki/eml_analyzer)
[![Coverage Status](https://coveralls.io/repos/github/ninoseki/eml_analyzer/badge.svg?branch=master)](https://coveralls.io/github/ninoseki/eml_analyzer?branch=master)
[![CodeFactor](https://www.codefactor.io/repository/github/ninoseki/eml_analyzer/badge)](https://www.codefactor.io/repository/github/ninoseki/eml_analyzer)

EML analyzer is an application to analyze the EML file which can:

- Analyze headers.
- Analyze bodies.
  - Extract IOCs (URLs, domains, IP addresses, emails) in bodies.
- Analyze attachments.
  - Identify whether attachments contain suspicious OLE files.

## Installation

### Docker

```bash
git clone https://github.com/ninoseki/eml_analyzer.git
cd eml_analyzer
docker build . -t eml_analyzer
docker run -i -d -p 8000:8000 eml_analyzer
```

The application is running at: http://localhost:8000/ in your browser.

### Docker Compose

```bash
git clone https://github.com/ninoseki/eml_analyzer.git
cd eml_analyzer
docker-compose up
```

### Docker vs. Docker compose

- Docker:
  - Run [Uvicorn](https://www.uvicorn.org/) and [SpamAssassin](https://spamassassin.apache.org/) in the same container. (The processes are managed by [Circus](https://circus.readthedocs.io/en/latest/))
- Docker Compose:
  - Run [Gunicorn](https://gunicorn.org/) and SpamAssassin in each container.

Thus Docker Compose is suitable for the production use.

### Heroku

Alternatively, you can deploy the application on Heroku.

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/ninoseki/eml_analyzer)

## ToDo

- [x] Support MSG format.
- [ ] In-depth attachments analysis by using oletools.
