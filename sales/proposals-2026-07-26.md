# Targeted Proposal Pack — 2026-07-26

These proposals are matched to currently visible small Python automation jobs. Before submitting, replace any bracketed details with the exact client URL, repository, or requested fields. Do not claim access to systems or data that have not been provided.

## 1. Config-driven CSV/JSON Instrument Parser

**Suggested fixed price:** USD 49  
**Suggested delivery:** 2 days

Hi,

I can build the parser so the field order, target names, data types, units, defaults, validation thresholds, and allowed values all live outside the core code in CSV or JSON configuration.

I already have a small public implementation of this exact architecture:
https://github.com/jhhjwei/codex-runner/tree/main/demos/config-driven-parser

For your project, I would adapt it to your real instrument records and deliver:

- CSV and JSON configuration support
- clean CSV or JSON output
- type conversion and validation
- row-level error reporting
- sample configuration and usage notes
- automated test using your anonymized sample

Before starting, I would confirm one input sample, one expected output sample, and how invalid rows should be handled. For a focused first version, I can deliver this as a USD 49 fixed-price task within 2 days.

Best,

## 2. Debug Existing Python Crawler

**Suggested fixed price:** USD 99 after initial code review  
**Suggested delivery:** 3 days

Hi,

I can review the existing crawler and isolate the three failure paths separately: JavaScript-rendered HTML, PDF discovery/download, and text-file decoding. I would avoid rewriting the whole project before identifying which layer is failing.

My proposed process is:

1. reproduce each failure with a small URL set;
2. record response status, content type, final URL, encoding, and extraction result;
3. keep requests/BeautifulSoup for static pages;
4. add a browser layer only for pages that actually require JavaScript;
5. normalize PDF and text downloads with deterministic filenames and error logs;
6. add a regression test or repeatable verification script.

A related public text-crawling sample is available here:
https://github.com/jhhjwei/codex-runner/tree/main/demos/public-web-text-scraper

If you can share the current repository and 3–5 representative public URLs, I can first confirm the root causes and then complete a focused repair for USD 99 within 3 days, assuming authentication is not required.

Best,

## 3. Windows Public Website Text Scraper

**Suggested fixed price:** USD 79  
**Suggested delivery:** 3 days

Hi,

I can create a small Windows-friendly Python utility that accepts a public URL, crawls only the approved page range, extracts visible text, and saves the result locally. The core crawler will use clear scope limits, reasonable delays, error reporting, and robots.txt checks.

I already have a public command-line sample showing the extraction and safety controls:
https://github.com/jhhjwei/codex-runner/tree/main/demos/public-web-text-scraper

For your requested version, I would add:

- URL input and Start button
- progress and completion status
- same-domain or approved-path limits
- text output in the application folder
- readable source code
- Windows packaging instructions or a compiled executable
- a short test checklist for Windows 10/11

For one password-free website with a stable structure, I can deliver the first usable version for USD 79 within 3 days. I would need the target URL and an example of the expected text output before starting.

Best,

## Submission checklist

- Open the actual project and replace generic wording with the client’s exact nouns.
- Keep only the deliverables requested by the client.
- Ask for anonymized samples, not credentials.
- Never promise JavaScript rendering, login automation, proxy rotation, or executable packaging unless it is included in the agreed scope.
- Use a milestone or platform escrow when available.
