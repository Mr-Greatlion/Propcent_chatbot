# PropScent AI – Phase 1: Listing URL Collection

## Overview

PropScent AI is an industry-grade real estate data collection system designed to
collect, validate, and structure property data from public real estate portals.

This submission demonstrates **Phase 1 – Listing URL Collection**, built using
Playwright + Python with a scalable, production-ready architecture.

## Phase 1 Objective

- Navigate public property listing pages
- Handle pagination reliably
- Extract **only valid listing URLs**
- Deduplicate URLs
- Store outputs in structured format

No demo hacks. No shortcuts.

---

## Architecture

### Entry Point

- `run_phase1.py`
  Controls the full Phase 1 execution lifecycle.

### Configuration Layer

- `config/sites.py`
  Defines portal-specific selectors and rules.
  Allows easy extension to new websites.

### Crawling Layer

- `crawler/browser.py`
  - Manages Playwright browser & context
- `crawler/navigator.py`
  - Handles pagination and page traversal
- `crawler/extractor.py`
  - Extracts listing URLs from each page

### Queue Layer

- `queue/url_queue.py`
  - Deduplicates URLs
  - Prevents re-processing

### Storage Layer

- `storage/json_store.py`
  - Persists collected URLs in JSON format

---

## Technology Stack

- Python 3.10+
- Playwright (Chromium)
- JSON-based storage (Phase 1)

---

## How to Run

### 1. Install dependencies
