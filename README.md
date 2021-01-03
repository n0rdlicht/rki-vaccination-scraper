---
home: true
sidebar: auto
lang: en-EN
footer: Made with ❤️ in Hamburg/Zurich
---

<ToggleDarkMode/>

# RKI Vaccination Monitoring

[![goodtables.io](https://goodtables.io/badge/github/n0rdlicht/rki-vaccination-scraper.svg)](https://goodtables.io/github/n0rdlicht/rki-vaccination-scraper)

Project to archive and track the [state level vaccination data](https://www.rki.de/DE/Content/InfAZ/N/Neuartiges_Coronavirus/Daten/Impfquoten-Tab.html) published by the Robert-Koch-Institut daily.

🏗️ A work in progress.

Experimental visualization: [Observable Notebook](https://observablehq.com/@n0rdlicht/vaccination-tracker-germany)

## The API

A simple Vercel-hosted API is available at [api.vaccination-tracker.app/v1/](https://api.vaccination-tracker.app/v1).

A plain request will respond with the full dataset `de-vaccinations`, paginated with 1000 entries per page.

- Data Package **Resources**: resources listed in [datapackage.json](datapackage.json) are exposed and can be accesses via

    ```sh
    GET https://api.vaccination-tracker.app/v1/<resource-name>
    ```
    e.g. `GET https://api.vaccination-tracker.app/v1/de-vaccinations`, currently available sets:
    - `de-vaccinations`: historized data as json
    - `de-vaccination-curren`: currently published version as json
- **Pagination**: `page=2` & `per_page=100` (defaults: `1` and `1000`)
- **Filter** by column: `<key>=<value>`, e.g. `?key=sum&geo=Hamburg` to only get summery values for the state of Hamburg
    - `sum`: All vaccinations
    - `ind_alter`: Indication by age
    - `ind_med`: Indication by medical condition
    - `ind_prof`: Indication by profession
    - `ind_pflege`: Indication by residents of nursing homes
    - `value`
    - `geo`: German state name or `Germany` for national data
    - `geotype`: either `state` for all states or `nation` for `Germany` entries
    - *Note: filtering by `date` is not supported yet*

### Example

Example request and response for all vaccinations by medical condition and publishing date in the state of Baveria:

```sh
twesterhuys@book ~ % curl --request GET 'https://api.vaccination-tracker.app/?key=ind_med&geo=Bayern'

{
  "dataset": "de-vaccinations",
  "time": "2021-01-03T15:38:55",
  "last_update": "2021-01-01T14:30",
  "last_published": "2021-01-02T14:30",
  "applied_filter": [{
    "geo": "Bayern"
  }, {
    "key": "ind_med"
  }],
  "per_page": 1000,
  "page": 0,
  "data": [{
    "geo": "Bayern",
    "iso-cc": "DE",
    "geotype": "state",
    "key": "ind_med",
    "value": 68.0,
    "date": "2020-12-27T00:00:00.000Z"
  }, {
    "geo": "Bayern",
    "iso-cc": "DE",
    "geotype": "state",
    "key": "ind_med",
    "value": 91.0,
    "date": "2020-12-28T00:00:00.000Z"
  }, {
    "geo": "Bayern",
    "iso-cc": "DE",
    "geotype": "state",
    "key": "ind_med",
    "value": 214.0,
    "date": "2020-12-29T00:00:00.000Z"
  }, {
    "geo": "Bayern",
    "iso-cc": "DE",
    "geotype": "state",
    "key": "ind_med",
    "value": 424.0,
    "date": "2020-12-30T00:00:00.000Z"
  }, {
    "geo": "Bayern",
    "iso-cc": "DE",
    "geotype": "state",
    "key": "ind_med",
    "value": 718.0,
    "date": "2020-12-31T00:00:00.000Z"
  }, {
    "geo": "Bayern",
    "iso-cc": "DE",
    "geotype": "state",
    "key": "ind_med",
    "value": 718.0,
    "date": "2021-01-01T00:00:00.000Z"
  }]
}
```

## The Data Package

1. Daily [GitHub Action](.github/workflows/main.yml) running a Frictionless Data Package Pipeline as defined in [pipeline-spec.yaml](pipeline-spec.yaml). Currently run manually, to be automated based on changes to [RKI website](https://www.rki.de/DE/Content/InfAZ/N/Neuartiges_Coronavirus/Daten/Impfquoten-Tab.html)
1. Resulting in a [combined CSV](data/de-vaccinations.csv) and [current day CSV](data/de-vaccinations-current.csv)
1. Metadata and validation can be done via `data validate` on [datapackage.json](datapackage.json)
1. D3.js visualization of data

### Updating the data

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