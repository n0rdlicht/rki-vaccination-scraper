---
home: true
title: Guide
sidebar: auto
lang: en-US
footer: Made with ❤️ in Hamburg/Zurich
---

<ToggleDarkMode/>

# RKI Vaccination Monitoring

> ⚠️ Currently undergoind refactoring due to major data source change, updating data will be back soon, see [#13](https://github.com/n0rdlicht/rki-vaccination-scraper/issues/13) for details.

[![goodtables.io](https://goodtables.io/badge/github/n0rdlicht/rki-vaccination-scraper.svg)](https://goodtables.io/github/n0rdlicht/rki-vaccination-scraper)

Project to archive and track the [state level vaccination data](https://www.rki.de/DE/Content/InfAZ/N/Neuartiges_Coronavirus/Daten/Impfquoten-Tab.html) published by the Robert-Koch-Institut daily.

🏗️ A work in progress.

<iframe width="100%" height="584" frameborder="0" src="https://observablehq.com/embed/@n0rdlicht/vaccination-tracker-germany?cell=viewof+geo&cell=viewof+indicator&cell=chart"></iframe>

Experimental visualization: [Observable Notebook](https://observablehq.com/@n0rdlicht/vaccination-tracker-germany)

## The API

A simple Vercel-hosted API is available at [api.vaccination-tracker.app/v1/](https://api.vaccination-tracker.app/v1/).

A plain request will respond with the full dataset `de-vaccinations`, paginated with 1000 entries per page.

### Resources

Data Package **Resources**: resources listed in [datapackage.json](datapackage.json) are exposed and can be accesses via

```sh
GET https://api.vaccination-tracker.app/v1/<resource-name>
```
e.g. `GET https://api.vaccination-tracker.app/v1/de-vaccinations`, currently available sets:
- `de-vaccinations`: historized data as json
- `de-vaccination-current`: currently published version as json
- `de-population-current`: population data from DeStatis

### Changelog

- Jan 4, 2021: Adds `quote` and `population` fields for comparison between different `geo`'s
- Jan 18, 2021: Complete refactor due to overhauled excel structure and additional data

### Pagination
Add `page=2` & `per_page=100` (defaults: `1` and `1000`)

Make sure to adapt these to your type of request.

### Filter / Values for `de-vaccinations` and `de-vaccinations-current`
By column: `<key>=<value>`, e.g. `?key=sum&geo=Hamburg` to only get summery values for the state of Hamburg

Most columns can be suffixed by `_initial` and `_booster` from `Jan 18` onward for more detailed values on the initial vaccination as well as the booster shots.

Values for `key`
- `sum`: All vaccinations
- `sum_initial_biontech` / `sum_initial_moderna`: Number of vaccinations in intial round for respective vaccinations by BioNTech or Moderna
- `delta_vortag`: Delta to the previous reported day
- `quote_initial` / `quote_booster`: rate of vaccination per 100, *only on entries with where `key` is `sum`*
- `ind_alter`: Indication by age
- `ind_med`: Indication by medical condition
- `ind_prof`: Indication by profession
- `ind_pflege`: Indication by residents of nursing homes

Other filters
- `geo`: German state name or `Germany` for national data
- `geotype`: either `state` for all states or `nation` for `Germany` entries
- `population`: number of residents in `geo`
- *Note: filtering by `date` is not supported yet and only available in de-vaccinations*

### Example

Example request and response for all vaccinations by medical condition and publishing date in the state of Baveria:

```sh
twesterhuys@book ~ % curl --request GET 'https://api.vaccination-tracker.app/v1/de-vaccinations?key=ind_med&geo=Bayern'

{
  "dataset": "de-vaccinations",
  "time": "2021-01-04T12:49:20",
  "last_update": "2021-01-03T11:32",
  "last_published": "2021-01-04T11:32",
  "applied_filter": [{
    "geo": "Bayern"
  }, {
    "key": "ind_med"
  }],
  "per_page": 1000,
  "page": 0,
  "data": [{
    "date": "2020-12-27T00:00:00.000Z",
    "geo": "Bayern",
    "key": "ind_med",
    "iso-cc": "DE",
    "geotype": "state",
    "value": 68,
    "population": 13124737,
    "quote": null
  }, {
    "date": "2020-12-28T00:00:00.000Z",
    "geo": "Bayern",
    "key": "ind_med",
    "iso-cc": "DE",
    "geotype": "state",
    "value": 91,
    "population": 13124737,
    "quote": null
  }, {
    "date": "2020-12-29T00:00:00.000Z",
    "geo": "Bayern",
    "key": "ind_med",
    "iso-cc": "DE",
    "geotype": "state",
    "value": 214,
    "population": 13124737,
    "quote": null
  }, {
    "date": "2020-12-30T00:00:00.000Z",
    "geo": "Bayern",
    "key": "ind_med",
    "iso-cc": "DE",
    "geotype": "state",
    "value": 424,
    "population": 13124737,
    "quote": null
  }, {
    "date": "2020-12-31T00:00:00.000Z",
    "geo": "Bayern",
    "key": "ind_med",
    "iso-cc": "DE",
    "geotype": "state",
    "value": 718,
    "population": 13124737,
    "quote": null
  }, {
    "date": "2021-01-01T00:00:00.000Z",
    "geo": "Bayern",
    "key": "ind_med",
    "iso-cc": "DE",
    "geotype": "state",
    "value": 718,
    "population": 13124737,
    "quote": null
  }, {
    "date": "2021-01-02T00:00:00.000Z",
    "geo": "Bayern",
    "key": "ind_med",
    "iso-cc": "DE",
    "geotype": "state",
    "value": 1091,
    "population": 13124737,
    "quote": null
  }, {
    "date": "2021-01-03T00:00:00.000Z",
    "geo": "Bayern",
    "key": "ind_med",
    "iso-cc": "DE",
    "geotype": "state",
    "value": 1280,
    "population": 13124737,
    "quote": null
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
make update # Fetch and merge todays data with existing data

# Validate Data Package (requires goodtables)
make validate

# To deactivate virtual environment
deactivate
```
