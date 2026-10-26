# Ireland Property Analysis

Analysis of publicly available Irish property data for validation, cleaning, and price-related exploration.

## About

This is a personal portfolio project that explores public Irish property data. I’m building it step by step to improve my Python, AI/ML, AWS, and software delivery skills.


The first goal is a tested Python pipeline that cleans property data and explains data-quality problems. I’ll then add a small Streamlit app, compare simple analysis with a local ML model, and run a container-based demo on AWS.


I’m learning from written guides and writing the code myself. AI tools help me understand errors and review my work. Results are for learning and exploration; an unusual value does not prove fraud.

## Project status
This project is still in progress. The core project structure, environment bootstrap, validation rules, and initial test coverage are in place, but the dataset processing and analysis pipeline is still being expanded.

## What has been implemented so far

### 1) Environment setup
Use [scripts/bootstrap.sh](scripts/bootstrap.sh) to set up the local Python environment. It requires Python 3.12 or 3.13, installs Poetry if needed, and uses the tracked `poetry.lock` to install the project and development dependencies into `.venv`. The script checks for a valid existing environment and recreates it if it is missing or broken.

From the repository root, run:

```bash
./scripts/bootstrap.sh
```

Activate the environment with `source .venv/bin/activate`. To run the tests, use `pytest`.

### 2) Property validation and custom exceptions
The project now contains a custom validation hierarchy in [src/exceptions.py](src/exceptions.py):
- `PropertyError` as the base exception
- `PropertyRawDataValidationError` for malformed raw property data

This is used by the raw listing schema in [src/schema.py](src/schema.py), which validates essential fields before accepting a property record. In particular, a property data object raises an exception when required fields such as `date_of_sale` or `price` are missing.

### 3) Immutable raw property records
The schema uses a frozen dataclass for the raw property record in [src/schema.py](src/schema.py). This means once a raw property listing has been built and validated, it cannot be mutated accidentally after processing.

This helps protect the integrity of the data as it moves through the analysis pipeline.

### 4) Tests for valid and invalid property data
The project includes fixture-driven validation tests in [tests/data_validation_tests.py](tests/data_validation_tests.py).

These tests cover:
- a valid property record is accepted without raising an exception
- missing `date_of_sale` raises `PropertyRawDataValidationError`
- missing `price` raises `PropertyRawDataValidationError`

The fixture-based approach keeps the tests readable and makes it easy to reuse a known-good dataset for multiple checks.

## Issues fixed by these changes
1. Bootstrap now handles a broken or invalid Poetry virtual environment by checking its health and rebuilding it if needed.
2. Validation exceptions are raised when property data is missing critical fields such as the sale date or price.
3. The bootstrap script makes the Python environment easier to recreate consistently.
4. The schema is frozen to prevent accidental mutation of processed raw data.
5. The project structure is now ready for continued development and validation work.

## Current focus
The next steps are to expand the raw data model, add more validation rules, and build the analysis pipeline for Irish property data.

## Example valid property record
A complete valid raw listing includes fields such as:
- Date of Sale
- Address
- County
- Eircode
- Price (€)
- VAT Exclusive flag
- Full market price flag
- Description of property
- Property size description

Example values from the project context:
- Date of Sale: 04/01/2010
- Address: 49 ballynakelly green, newcastle
- County: Dublin
- Price: €499,600.00
- VAT Exclusive: Yes
- Description: New Dwelling house /Apartment
- Property Size Description: greater than 125 sq metres

This project is still under active development.

## Data sources:

1. sales from here: https://www.propertypriceregister.ie/website/npsra/ppr/npsra-ppr.nsf/Downloads/PPR-ALL.zip/$FILE/PPR-ALL.zip
2. Rent from here: https://rtb.ie/data-insights/rtb-data-hub/rtb-esri-rent-index-data-set