# RKI Vaccination Monitoring

[![goodtables.io](https://goodtables.io/badge/github/n0rdlicht/rki-vaccination-scraper.svg)](https://goodtables.io/github/n0rdlicht/rki-vaccination-scraper)

Project to archive the [state level vaccination data](https://www.rki.de/DE/Content/InfAZ/N/Neuartiges_Coronavirus/Daten/Impfquoten-Tab.html) published by the Robert-Koch-Institut daily.

🏗️ A work in progress.

Experimental visualization: [Observable Notebook](https://observablehq.com/@n0rdlicht/vaccination-tracker-germany)

## Technical setup

1. Daily [GitHub Action](.github/workflows/main.yml) running a Frictionless Data Package Pipeline as defined in [pipeline-spec.yaml](pipeline-spec.yaml). Currently run manually, to be automated based on changes to [RKI website](https://www.rki.de/DE/Content/InfAZ/N/Neuartiges_Coronavirus/Daten/Impfquoten-Tab.html)
1. Resulting in a [combined CSV](data/de-vaccinations.csv) and [current day CSV](data/de-vaccinations-current.csv)
1. Metadata and validation can be done via `data validate` on [datapackage.json](datapackage.json)
1. D3.js visualization of data

### To update the data

Either trigger the [GitHub action "Update Data Package"](https://github.com/n0rdlicht/rki-vaccination-scraper/actions) or run locally

```sh
# Get the code
git clone https://github.com/n0rdlicht/rki-vaccination-scraper.git
cd rki-vaccination-scraper

# Activate a virtual environment and install dependencies
virtualenv env
. env/bin/activate
pip install -Ur requirements.txt

# Run all pipelines
make

# or
make fetch # Only fetch todays data
make update # Merge todays data with existing data

# Validate Data Package (requires goodtables)
make validate

# To deactivate virtual environment
deactivate
```