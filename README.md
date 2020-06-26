# EML analyzer

[![Build Status](https://travis-ci.com/ninoseki/eml_analyzer.svg?branch=master)](https://travis-ci.com/ninoseki/eml_analyzer)
[![Coverage Status](https://coveralls.io/repos/github/ninoseki/eml_analyzer/badge.svg?branch=master)](https://coveralls.io/github/ninoseki/eml_analyzer?branch=master)
[![CodeFactor](https://www.codefactor.io/repository/github/ninoseki/eml_analyzer/badge)](https://www.codefactor.io/repository/github/ninoseki/eml_analyzer)

EML analyzer is an application for analyzing the EML file which can:

- Analyze headers.
- Analyze bodies.
  - Extract IOCs (URLs, domains, IP addresses, emails) in bodies.
- Analyze attachments.
  - Identify whether attachments contain suspicious OLE files.

And also it analyzes the EML file by using [SpamAssassin](https://spamassassin.apache.org/).

## Installation

### Docker

```bash
git clone https://github.com/ninoseki/eml_analyzer.git
cd eml_analyzer
docker build . -t elm_analyzer
docker run -i -d -p 8000:8000 elm_analyzer
```

The application is running at: http://localhost:8000/ in your browser.
