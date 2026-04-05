# ireland-property-analysis
analysis of puplicly available data about irish properties.

A robust data engineering pipeline designed to ingest, clean, and validate the Irish Property Price Register (PPR). This project moves beyond simple EDA by implementing a Data Contract approach, ensuring that unstructured address data is transformed into high-quality, verifiable features.

[![AWS CodeCommit Mirror](https://github.com/youssefabdalla/ireland-property-analysis/actions/workflows/mirror.yml/badge.svg)](https://github.com/youssefabdalla/ireland-property-analysis/actions/workflows/mirror.yml)

## What I did so far:
1. got the data from [the Irish property register as zip file](https://www.propertypriceregister.ie/website/npsra/ppr/npsra-ppr.nsf/Downloads/PPR-ALL.zip/$FILE/PPR-ALL.zip)
_following is still in notebook_
2. cleaned the column names
3. cleaned the price. So removed everything that isn't a digit or decimal point
4. created a new boolean column for VAT exclusive
5. the data is huge so i took only dublin
6. Parsed the address using deepparse, so instead of a string i get dictionary of house number, street name, unit ... etc
7. Found that parsing string by string is very slow, so i parse addresses in batches
8. save result to a csv
_The validation_
9. Using great expectations i validate the input data
10. use data assistant of great expectations to create initial rule to judge the quality of the input data
11. created my own rules as json
12. ran them on the data

## main structure so far

ireland-property-analysis/
├── data/
│   ├── raw/                  # Original "As-Is" CSV (Ignored by Git)
│   └── processed/            # Cleaned Dublin-only data with parsed addresses
├── gx/                       # Great Expectations engine
│   ├── expectations/         # THE CONTRACT: JSON definitions of "Good Data"
│   └── uncommitted/          # Validation results & HTML reports (Ignored by Git)
├── notebooks/                # R&D, Exploratory Data Analysis, and Prototyping
├── src/                      # Production-grade Python scripts
│   ├── ingest/               # Download & extraction logic
│   └── validate/             # Headless validation runner
└── README.md

